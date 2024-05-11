# Library Management System

The Library Management System is a web application that allows general users to browse, request, and access e-books from an online library, while a librarian can manage sections, e-books, and user access. It incorporates features such as search functionality, daily reminders, monthly activity reports, APIs for CRUD operations, and input validation.

## Technologies Used

- Flask 3.0.2 for app routing, template rendering, and redirecting.
- Flask-SQLAlchemy for connecting the SQLite database as a server with the Flask application.
- Celery [Redis] for caching and scheduling asynchronous tasks.
- Flask_JWT_Extended for tokenization.
- Vue.js for frontend tasks.
- Bootstrap for styling.

## Database Schema Design

The application uses the following database tables:

- Users
- Books
- Sections
- BookRequests
- UserBooks
- Feedback

## API Design

The application provides the following API endpoints:

1. **Authentication and Authorization**
  - `/register`: User registration
  - `/login`: User login
  - `/refresh`: Refresh access tokens
  - `/logout`: User logout

2. **Sections and Books Management**
  - `/sections`: Create, update, and delete sections (categories)
  - `/books`: Create, update, and delete books
  - `/books/read/<int:book_id>/content`: Retrieve the content of a book
  - `/sections/<int:section_id>/books`: Get a list of books for a specific section

3. **User Management**
  - `/users/all`: Retrieve all user information
  - `/users/<int:user_id>`: Retrieve information for a specific user

4. **User Book Management**
  - `/users/<int:user_id>/books`: Retrieve a list of books borrowed by a user
  - `/users/<int:user_id>/books`: Issue a book to a user (librarian)
  - `/users/<int:user_id>/books/<int:book_id>`: Update the return date or revoke a book from a user (librarian)

5. **Feedback Management**
  - `/feedback/users/<int:user_id>/books/<int:book_id>/feedbacks`: Submit feedback for a book (user)
  - `/feedback/users/<int:user_id>/books/<int:book_id>/feedbacks/<int:feedback_id>`: Retrieve and update feedback for a specific book (user)

6. **Book Request Management**
  - `/request/make/<int:book_id>`: Request a book (user)
  - `/request/view`: View book requests (user)
  - `/request`: Retrieve pending book requests (librarian)
  - `/request/approve/<int:request_id>`: Approve a book request (librarian)
  - `/request/deny/<int:request_id>`: Deny a book request (librarian)

7. **Analytics and Statistics**
  - `/analytics/section-distribution`: Retrieve section-wise book distribution
  - `/analytics/user-login-activity`: Retrieve user login activity within a specified date range
  - `/book_requests/status_counts`: Retrieve counts of issued, denied, and pending book requests

## Architecture and Features

The project folder named "Library Management System" consists of all the required files, including two folders named "frontend" and "backend" containing files such as `config.py`, `controllers.py`, `database.py`, `models.py`, `tasks.py`, Vue components, `App.vue`, routers, etc.

This application allows users to browse and request e-books from an online library. Librarians can manage sections, e-books, and user access. The application also features daily reminders, monthly activity reports, and input validation.

## Video Demonstration

A video demonstration of the application is available at the following link:

[Video Link](https://www.canva.com/design/DAGCrJmC9lA/Ojd2u5rx0qf7G_WCwnoiIQ/watch?utm_content=DAGCrJmC9lA&utm_campaign=designshare&utm_medium=link&utm_source=editor)
