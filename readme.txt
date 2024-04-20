# Web App Setup Guide

## Introduction
This guide provides step-by-step instructions for setting up the environment and servers required to run the web application.

## Setup Instructions

1. **Setting up the Flask server:**
   - Open a new terminal tab in Linux.
   - Navigate to the "Backend" directory.
   - Start the Flask server by executing:
     ```
     cd Backend
     python3 main.py
     ```

2. **Setting up the Frontend Server:**
   - Open another terminal tab in Linux.
   - Navigate to the "Frontend" directory.
   - Start the Frontend server by executing:
     ```
     cd Frontend
     npm run serve
     ```

3. **Setting up the Redis server:**
   - Open a new terminal tab.
   - Start the Redis server by executing:
     ```
     redis-server
     ```

4. **Setting up the MailHog server:**
   - Open another terminal tab.
   - Start the MailHog server by executing:
     ```
     ~/go/bin/MailHog
     ```

5. **Setting up Celery Worker and Celery Beat:**
   - Open a new terminal tab.
   - Start the Celery Workers and Beat together by executing:
     ```
     celery -A tasks.celery worker -l info -B
     ```

## Additional Notes
- Ensure that all dependencies are installed before starting the servers.
- You may need to configure the servers based on your specific requirements.
- Make sure to check the logs for any errors during the setup process.

Follow these instructions carefully to set up the environment and servers for your web application.

