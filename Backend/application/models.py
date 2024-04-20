"""
Module for Database
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    DateTime,
    func,
)
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from pytz import timezone
from datetime import datetime

# from flask_security import RoleMixin
db = SQLAlchemy()

ist = timezone("Asia/Kolkata")  # Set the timezone to Indian Standard Time (IST)


class Role(db.Model):
    """Table for Roles"""

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    users = db.relationship("User", backref="role")  # Corrected backref


class User(db.Model, UserMixin):
    """Table for User"""

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    confirmed_at = Column(DateTime, nullable=False, default=datetime.now())
    last_logged_in =  Column(DateTime, nullable=False, default=datetime.now())
    last_reminder_sent = Column(DateTime, nullable=False, default=datetime.now())
    role_id = Column(String, ForeignKey("role.id"), nullable=False)
    book_requests = db.relationship("BookRequest", backref="user" , cascade="all, delete-orphan")

    def get_id(self):
        """Get the user ID."""
        return self.username

    def __repr__(self):
        """Representation of the User object."""
        return f"<User {self.username}>"

    def set_password(self, password):
        """Set user's password after hashing."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the user's hashed password."""
        return check_password_hash(self.password, password)

    @classmethod
    def get_user_by_username(cls, username):
        """Get a user by username."""
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_user_by_email(cls, email):
        """Get user by email"""
        return cls.query.filter_by(email=email).first()

    def save(self):
        """Save the user to the database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the user from the database."""
        db.session.delete(self)
        db.session.commit()


class TokenBlocklist(db.Model):
    """
    Table for Creating TokenBlocklist
    """

    id = Column(Integer, primary_key=True)
    jti = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f"<Token {self.jti}>"

    def save(self):
        """
        function to save details into database
        """
        db.session.add(self)
        db.session.commit()


class Section(db.Model):
    """Table for Different Books Categories"""

    section_id = Column(Integer, primary_key=True)
    section_name = Column(String, nullable=False)
    description = Column(String)
    date_created = Column(DateTime, nullable=False, default=datetime.now())
    books = db.relationship("Book", backref="section")

    def __repr__(self):
        return f"<Section {self.section_name}>"
    
    def serialize(self):
        return {
            "id": self.section_id,
            "section_name": self.section_name,
            "description": self.description,
        }


class Book(db.Model):
    """Table for storing Different Books Details"""

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    book_name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    section_id = Column(Integer, ForeignKey("section.section_id",ondelete="CASCADE"), nullable=False)
    user_books = db.relationship("UserBook", backref="book" , cascade="all, delete-orphan")
    path = Column(String, nullable=False)

    book_requests = db.relationship("BookRequest", backref="book" , cascade="all, delete-orphan") 

    def __repr__(self):
        return f"<Book {self.book_name}>"


class BookRequest(db.Model):
    """Table for handling book requests"""

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("book.book_id"), nullable=False)
    request_date = Column(DateTime, nullable=False, default=datetime.now())
    status = Column(String, nullable=False, default="pending")  # Status: pending, issued, denied

    def __repr__(self):
        return f"<BookRequest {self.id}>"


class UserBook(db.Model):
    """Table for books issued by User"""

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    book_id = Column(Integer, ForeignKey("book.book_id"), primary_key=True)
    issued_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)
    expiry_date = Column(DateTime, nullable=False)
    status = Column(
        String, nullable=False, default="issued"
    )  # Status: issued, returned

    user = db.relationship("User", backref="user_books")

    # Explicitly specify foreign keys for the feedback relationship
    feedback_id = Column(Integer, ForeignKey("feedback.feedback_id"))
    feedback = db.relationship("Feedback", foreign_keys=[feedback_id])

    def __repr__(self):
        return f"<UserBook {self.id}>"


class Feedback(db.Model):
    """Table for Feedback on Books Issued by User"""

    feedback_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_book.user_id"), nullable=False)
    book_id = Column(Integer, ForeignKey("user_book.book_id"), nullable=False)
    rating = Column(Integer, nullable=True)
    comments = Column(String)
    date_submitted = Column(DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f"<Feedback {self.feedback_id}>"
