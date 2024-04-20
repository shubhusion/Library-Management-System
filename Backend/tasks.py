"""
Module: tasks.py

This module contains Celery tasks for sending reminder messages to inactive users
and monthly reports to active users via email. It also includes setup for periodic tasks.

Functions:
    - send_reminder_webhooks(): Sends reminder messages to inactive users via webhook.
    - send_monthly_reports(): Sends monthly reports to active users via email.
    - setup_intervalTASK(): Sets up periodic tasks for reminders and reports.

"""

import os

# import csv
from datetime import datetime, timedelta, date
import requests
from collections import defaultdict
from main import celery, cache
from application.models import User, Book, UserBook, Section
from jinja2 import Template
from weasyprint import HTML
from mail_config import send_email


@celery.on_after_finalize.connect
def setup_intervalTASK(sender, **kwargs):
    sender.add_periodic_task(
        # Send a remainder at 5:30pm IST of every day
        # crontab(minute=30, hour=17),
        60,
        send_reminder_webhooks.s(),
        name="Daily reminder",
    )

    sender.add_periodic_task(
        # Send the monthly report at 5:30pm IST of every month
        # crontab(minute=30, hour=17, day_of_month=25),
        10,
        send_monthly_reports.s(),
        name="Monthly Report",
    )


@celery.task(name="tasks.send_reminder_webhooks")
def send_reminder_webhooks():
    """
    Send reminder messages to inactive users via webhook.

    This function retrieves inactive users from the database and sends them reminder
    messages via a specified webhook URL.

    Parameters:
        None

    Returns:
        None
    """
    # yesterday = datetime.now() - timedelta(days=1)
    one_hour_ago = datetime.now() - timedelta(hours=1)
    inactive_users = User.query.filter(User.last_logged_in <= one_hour_ago).all()

    # Dictionary to store the number of reminders sent to each user
    reminders_sent_count = defaultdict(int)

    for user in inactive_users:
        if user.last_logged_in is None:
            continue  # Skip users without activity data

        # Define the maximum number of reminders allowed for each user
        max_reminders = 3  # Adjust this value as needed

        # Check if the maximum number of reminders has been reached for this user
        if reminders_sent_count[user.id] >= max_reminders:
            continue  # Skip sending reminders to this user

        webhook_url = "https://chat.googleapis.com/v1/spaces/AAAA9So9EJ4/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=tnga0dPTPlE1Lpqe2XvLnrb9cGa9wlfWLJAXGuy1EsU"  # Update with your actual webhook URL
        payload = {
            "text": f"{user.username} Please visit our library site",
        }

        response = requests.post(webhook_url, json=payload, timeout=10)
        print(response.status_code)
        if response.status_code == 200:
            reminders_sent_count[
                user.id
            ] += 1  # Increment the reminders sent count for this user
            print("Success")


@celery.task()
def send_monthly_reports():
    """Send monthly reports to active users via email.
    This function retrieves active users from the database and sends them monthly reports containing their booking information as a PDF attachment.
    Parameters: None
    Returns: str: A message indicating the success of the task.
    """
    users = User.query.filter_by(active=True).all()
    print(f"Found {len(users)} active users.")

    for user in users:
        if user.username == "admin":
            print(f"Skipping admin user: {user.username}")
            continue

        user_books = UserBook.query.filter_by(user_id=user.id).all()
        print(f"Retrieved {len(user_books)} books for user: {user.username}")

        if len(user_books) == 0:
            print(f"User {user.username} has no books. Skipping.")
            continue

        month = date.today().strftime("%B")
        e = user.email
        u = {"logged": user.confirmed_at, "email": e}
        u["username"] = user.username
        filepath = f"static/monthly_reports/monthly_report_{str(u['username'])}.pdf"

        if not os.path.exists("static/monthly_reports/"):
            os.mkdir(path="static/monthly_reports/")

        with open(r"templates/monthly_report.html", encoding="utf8") as file:
            msg_template = Template(file.read())

        with open(r"templates/pdf.html", encoding="utf8") as file:
            pdf_template = Template(file.read())

        booking_info_text = []
        for user_book in user_books:
            book = Book.query.get(user_book.book_id)
            print(f"Retrieved book: {book.book_name} for user: {user.username}")

            section = Section.query.get(book.section_id)
            print(
                f"Retrieved section: {section.section_name} for book: {book.book_name}"
            )

            booking_info = {
                "book_name": book.book_name,
                "author": book.author,
                "section_name": section.section_name,
            }
            booking_info_text.append(booking_info)

        print(f"Booking info for user {user.username}: {booking_info_text}")

        pdf_html = HTML(
            string=pdf_template.render(
                user=u, booking_info=booking_info_text, month=month
            )
        )
        pdf_html.write_pdf(target=filepath)
        print(f"PDF generated for user {user.username} at {filepath}")

        send_email(
            to=e,
            subject="Monthly report",
            attachment=filepath,
            msg=msg_template.render(username=u["username"]),
        )
        print(f"Email sent to {user.username} ({user.email})")

    return "success"
