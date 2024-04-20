"""
Module for Authorisation & Authentication
"""

import os
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import (  # type: ignore
    create_access_token,
    create_refresh_token,
    JWTManager,
    get_jwt,
    jwt_required,
    get_jwt_identity,
    current_user,
    get_current_user,
)
from sqlalchemy import func
from application.models import (
    User,
    TokenBlocklist,
    Section,
    db,
    Book,
    User,
    UserBook,
    Feedback,
    BookRequest,
)
from application.helpers import role_required
from application.schemas import UserSchema

api_bp = Blueprint("api", __name__)
jwt = JWTManager()


# ---------------------------------------------- USER AUTHENTICATION & RELATED APIS ----------------------------------------
@api_bp.post("/register")
def registeruser():
    """
    function for Adding a new user
    """
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role_id")

    if not username or not email or not password or not role:
        return jsonify({"message": "Missing required fields"}), 400

    user = User.get_user_by_username(username=username)

    if user:
        return jsonify({"message": "Username already taken"}), 400

    user = User.get_user_by_email(email=email)

    if user:
        return jsonify({"message": "Email already registered"}), 400

    new_user = User(
        username=username,
        email=email,
        role_id=role,
    )

    new_user.set_password(password=data.get("password"))
    new_user.save()

    return jsonify({"Message": "User Registered Successfully "}), 200


@api_bp.post("/login")
def login_user():
    """
    Function for logging in an existing user
    """
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    user = User.get_user_by_username(username=username)

    if user and (user.check_password(password=password) or user.password == password):
        # Update last login time
        user.last_logged_in = datetime.now()
        db.session.commit()

        # Generate access and refresh tokens
        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)

        return (
            jsonify(
                {
                    "message": "Logged In",
                    "tokens": {"access": access_token, "refresh": refresh_token},
                }
            ),
            200,
        )
    return jsonify({"error": "Invalid username or password"}), 400


@api_bp.get("/refresh")
@jwt_required()
def refresh_access():
    """
    refresh token
    """
    identity = get_jwt_identity()

    new_access_token = create_access_token(identity=identity)

    return jsonify({"access_token": new_access_token})


@api_bp.get("/whoami")
@jwt_required()
def whoami():
    claims = get_jwt()
    return jsonify(
        {
            "id":current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "role_id": current_user.role_id,
        }
    )


@api_bp.get("/logout")
@jwt_required()
def logout_user():
    """
    Function to logout
    """
    jwt = get_jwt()

    jti = jwt["jti"]

    token_b = TokenBlocklist(jti=jti)

    token_b.save()

    return jsonify({"message": "Logged Out Successfully"}), 200


# ---------------------------------------------------- SECTIONS CRUD APIS ----------------------------------------------------


@api_bp.route("/sections", methods=["GET", "POST", "OPTIONS"])
@jwt_required()
def handle_sections():
    """
    Handle requests related to sections.

    Returns:
        Flask Response: Serialized data for all sections or a specific section.

    Raises:
        HTTPException: If a section with the given ID does not exist.
    """
    if request.method == "OPTIONS":
        return "", 200  # Respond to preflight requests with 200 OK

    if request.method == "GET":
        sections = Section.query.all()
        return jsonify([section.serialize() for section in sections])

    if request.method == "POST":

        @role_required("librarian")
        def create_section():
            """
            Create a new section.

            Returns:
                Flask Response: Confirmation message and status code.

            Raises:
                HTTPException: If required fields are missing in the request.
            """
            data = request.get_json()
            section_name = data.get("section_name")
            description = data.get("description")

            if not section_name or not description:
                return jsonify({"message": "Missing required fields"}), 400

            section = Section(section_name=section_name, description=description)
            db.session.add(section)
            db.session.commit()

            return jsonify({"message": "Section created successfully"}), 201

        return create_section()


@api_bp.route("/sections/<int:section_id>", methods=["GET", "PUT", "DELETE", "OPTIONS"])
@jwt_required()
def handle_section(section_id):
    """
    Handle requests related to a specific section.

    Args:
        section_id (int): The ID of the section.

    Returns:
        Flask Response: Serialized data for the section.

    Raises:
        HTTPException: If the section with the given ID does not exist.
    """
    if request.method == "OPTIONS":
        return "", 200  # Respond to preflight requests with 200 OK

    section = Section.query.get_or_404(section_id)

    if request.method == "GET":
        return jsonify(section.serialize())

    if request.method == "PUT":

        @role_required("librarian")
        def update_section():
            """
            Update an existing section.

            Returns:
                Flask Response: Confirmation message.

            Raises:
                HTTPException: If the section with the given ID does not exist.
            """
            data = request.get_json()
            section.section_name = data.get("section_name", section.section_name)
            section.description = data.get("description", section.description)
            db.session.commit()
            return jsonify({"message": "Section updated successfully"})

        return update_section()

    if request.method == "DELETE":

        @role_required("librarian")
        def delete_section():
            """
            Delete a section.

            Returns:
                Flask Response: Confirmation message.

            Raises:
                HTTPException: If the section with the given ID does not exist.
            """
            db.session.delete(section)
            db.session.commit()
            return jsonify({"message": "Section deleted successfully"})

        return delete_section()


# ------------------------------------------------- BOOKS CRUD APIS -------------------------------------------------------------


@api_bp.route("/books", methods=["GET", "POST"])
@jwt_required()
def books():
    """
    Endpoint for retrieving all books or creating a new book.

    GET: Retrieves all books.
    POST: Creates a new book.

    Requires JWT token for authorization.
    """
    if request.method == "GET":
        bks = Book.query.all()
        return jsonify(
            [
                {
                    "book_id": book.book_id,
                    "book_name": book.book_name,
                    "path": book.path,
                    "author": book.author,
                    "section_id": book.section_id,
                }
                for book in bks
            ]
        )

    if request.method == "POST":
        return create_book()


@api_bp.route("/books/<int:book_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def book(book_id):
    """
    Endpoint for retrieving, updating, or deleting a specific book.

    GET: Retrieves a specific book.
    PUT: Updates a specific book.
    DELETE: Deletes a specific book.

    Requires JWT token for authorization.
    """
    bk = Book.query.get_or_404(book_id)

    if request.method == "GET":
        return jsonify(
            {
                "book_id": bk.book_id,
                "book_name": bk.book_name,
                "path": bk.path,
                "author": bk.author,
                "section_id": bk.section_id,
            }
        )

    if request.method == "PUT":
        return update_book(book_id)

    if request.method == "DELETE":
        return delete_book(book_id)


@role_required("librarian")
def create_book():
    """
    Creates a new book.

    Requires 'Librarian' role for authorization.
    """
    data = request.get_json()
    book_name = data.get("book_name")
    path = data.get("path")
    author = data.get("author")
    section_id = data.get("section_id")

    if not book_name or not path or not author or not section_id:
        return jsonify({"message": "Missing required fields"}), 400

    bk = Book(book_name=book_name, path=path, author=author, section_id=section_id)
    db.session.add(bk)
    db.session.commit()

    return jsonify({"message": "Book created successfully"}), 201


@role_required("librarian")
def update_book(book_id):
    """
    Updates an existing book.

    Requires 'Librarian' role for authorization.
    """
    data = request.get_json()
    bk = Book.query.get(book_id)  # Retrieve the book object using book_id
    if bk:
        bk.book_name = data.get("book_name", bk.book_name)
        bk.path = data.get("path", bk.path)
        bk.author = data.get("author", bk.author)
        bk.section_id = data.get("section_id", bk.section_id)
        db.session.commit()
        return jsonify({"message": "Book updated successfully"})
    else:
        return jsonify({"message": "Book not found"})


@role_required("librarian")
def delete_book(book_id):
    """
    Deletes an existing book.

    Requires 'Librarian' role for authorization.
    """
    bk = Book.query.get(book_id)  # Retrieve the book object using book_id
    if bk:
        db.session.delete(bk)
        db.session.commit()
        return jsonify({"message": "Book deleted successfully"})
    else:
        return jsonify({"message": "Book not found"})


@api_bp.route("/books/read/<int:book_id>/content", methods=["GET"])
def get_book_content(book_id):
    """
    Retrieves the content of a book.

    Requires 'Librarian' role for authorization.
    """
    book = Book.query.get(book_id)  # Retrieve the book object using book_id
    if book:
        if book.path:
            file_path = book.path
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                return jsonify({"content": content})
            else:
                return jsonify({"message": "File not found"})
        else:
            return jsonify({"message": "Book content path not specified"})
    else:
        return jsonify({"message": "Book not found"})


@api_bp.route("/sections/<int:section_id>/books", methods=["GET"])
def get_books_for_section(section_id):
    """
    Get Books Details Sectionwise
    """
    books = Book.query.filter_by(section_id=section_id).all()
    books_data = [
        {
            "book_id": book.book_id,
            "book_name": book.book_name,
            "author": book.author,
            "path": book.path,
        }
        for book in books
    ]
    return jsonify(books_data)


# --------------------------------------------- USER RELATED APIS ----------------------------------------------------


@api_bp.get("/users/all")
@jwt_required()
def getusers():
    """
    function for retrieving all users from the Database
    """
    page = request.args.get("page", default=1)
    per_page = request.args.get("per_page", default=2, type=int)

    users = User.query.paginate(page=page, per_page=per_page)

    result = UserSchema().dump(users, many=True)

    return jsonify({"users": result}), 200


@api_bp.get("/users/<int:user_id>")
@jwt_required()
def get_user_by_id(user_id):
    """
    Function for retrieving a user by ID from the Database
    """
    user = User.query.get_or_404(user_id)
    result = UserSchema().dump(user)
    return jsonify({"user": result}), 200


# ---------------------------------------- User Books APIs ---------------------------------------------------------------------
@api_bp.route("/users/<int:user_id>/books", methods=["GET", "POST"])
@jwt_required()
def user_books(user_id):
    """
    Endpoint to handle GET and POST requests related to user's books.

    Args:
        user_id (int): The ID of the user whose books are being accessed.

    Returns:
        JSON: Response containing user's books data or appropriate message.
    """
    user = User.query.get_or_404(user_id)

    if request.method == "GET":
        if get_jwt_identity() == user.id or role_required("Librarian"):
            user_books = UserBook.query.filter_by(user_id=user_id).all()
            return jsonify(
                [
                    {
                        "user_id": book.user_id,
                        "book_id": book.book_id,
                        "issued_date": book.issued_date,
                        "return_date": book.return_date,
                        "expiry_date": book.expiry_date,
                    }
                    for book in user_books
                ]
            )
        else:
            return jsonify({"message": "Unauthorized access"}), 403

    if request.method == "POST":
        data = request.get_json()
        book_id = data.get("book_id")
        days_to_issue = data.get("days_to_issue")

        if not book_id or not days_to_issue:
            return jsonify({"message": "Missing required fields"}), 400

        expiry_date = datetime.now() + timedelta(days=days_to_issue)

        user_book = UserBook(
            user_id=user_id,
            book_id=book_id,
            issued_date=datetime.now(),
            expiry_date=expiry_date,
        )
        db.session.add(user_book)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Book issued successfully",
                    "expiry_date": expiry_date.strftime("%Y-%m-%d"),
                }
            ),
            201,
        )


@api_bp.route("/users/<int:user_id>/books/<int:book_id>", methods=["PUT", "DELETE"])
@jwt_required()
def user_book(user_id, book_id):
    """
    Endpoint to handle PUT and DELETE requests related to a specific user book.

    Args:
        user_id (int): The ID of the user whose book is being accessed.
        book_id (int): The ID of the book being accessed.

    Returns:
        JSON: Response confirming the action performed on the book.
    """
    user_book = UserBook.query.filter_by(
        user_id=user_id, book_id=book_id
    ).first_or_404()

    if request.method == "PUT":

        @role_required("Librarian")
        def update_user_book():
            data = request.get_json()
            user_book.return_date = data.get("return_date", user_book.return_date)
            user_book.expiry_date = data.get("expiry_date", user_book.expiry_date)
            db.session.commit()

            return jsonify({"message": "User book updated successfully"})

        return update_user_book()

    if request.method == "DELETE":

        @role_required("Librarian")
        def revoke_book():
            db.session.delete(user_book)
            db.session.commit()

            return jsonify({"message": "Book access revoked successfully"})

        return revoke_book()

    # ------------------------------------------FEEDBACK APIs -------------------------------------------------------------


@api_bp.route(
    "/feedback/users/<int:user_id>/books/<int:book_id>/feedbacks",
    methods=["GET", "POST"],
)
@jwt_required()
def feedbacks(user_id, book_id):
    """
    Retrieve or submit feedback for a specific book by a user.

    Args:
        user_id (int): The ID of the user.
        book_id (int): The ID of the book.

    Returns:
        JSON: Feedback data or success message.
    """
    user = User.query.get_or_404(user_id)
    book = Book.query.get_or_404(book_id)

    if request.method == "GET":
        if get_jwt_identity() == user.id or role_required("Librarian"):
            feedbacks = Feedback.query.filter_by(user_id=user_id, book_id=book_id).all()
            return jsonify(
                [
                    {
                        "feedback_id": feedback.feedback_id,
                        "user_id": feedback.user_id,
                        "book_id": feedback.book_id,
                        "rating": feedback.rating,
                        "comments": feedback.comments,
                        "date_submitted": feedback.date_submitted,
                    }
                    for feedback in feedbacks
                ]
            )
        else:
            return jsonify({"message": "Unauthorized access"}), 403

    if request.method == "POST":
        data = request.get_json()
        rating = data.get("rating")
        comments = data.get("comments")

        if not rating or not comments:
            return jsonify({"message": "Missing required fields"}), 400

        feedback = Feedback(
            user_id=user_id, book_id=book_id, rating=rating, comments=comments
        )
        db.session.add(feedback)
        db.session.commit()

        return jsonify({"message": "Feedback submitted successfully"}), 201


@api_bp.route(
    "/feedback/users/<int:user_id>/books/<int:book_id>/feedbacks/<int:feedback_id>",
    methods=["GET", "PUT"],
)
@jwt_required()
def feedback(user_id, book_id, feedback_id):
    """
    Retrieve or update specific feedback for a book by a user.

    Args:
        user_id (int): The ID of the user.
        book_id (int): The ID of the book.
        feedback_id (int): The ID of the feedback.

    Returns:
        JSON: Feedback data or success message.
    """
    feedback = Feedback.query.filter_by(
        user_id=user_id, book_id=book_id, feedback_id=feedback_id
    ).first_or_404()

    if request.method == "GET":
        if get_jwt_identity() == user_id or role_required("Librarian"):
            return jsonify(
                {
                    "feedback_id": feedback.feedback_id,
                    "user_id": feedback.user_id,
                    "book_id": feedback.book_id,
                    "rating": feedback.rating,
                    "comments": feedback.comments,
                    "date_submitted": feedback.date_submitted,
                }
            )
        else:
            return jsonify({"message": "Unauthorized access"}), 403

    if request.method == "PUT":
        if get_jwt_identity() == user_id:
            data = request.get_json()
            feedback.rating = data.get("rating", feedback.rating)
            feedback.comments = data.get("comments", feedback.comments)
            db.session.commit()

            return jsonify({"message": "Feedback updated successfully"})
        else:
            return jsonify({"message": "Unauthorized access"}), 403


# ------------------------------------------ BOOK ISSUE/ ACCEPT / DENY / READ BOOK CONTENT ---------------------------------------


@api_bp.route("/request", methods=["GET"])
@jwt_required()
@role_required("librarian")
def requests():
    """
    Retrieve all pending book requests.

    Returns:
        JSON response containing data of pending requests.
    """
    pending_requests = BookRequest.query.filter_by(status="pending").all()
    requests_data = [
        {
            "id": request.id,
            "user_id": request.user_id,
            "book_id": request.book_id,
            "status": request.status,
        }
        for request in pending_requests
    ]
    return jsonify(requests_data)


@api_bp.route("/request/approve/<int:request_id>", methods=["POST"])
@role_required("librarian")
def approve_request(request_id):
    """
    Approve a book request and issue the book to the user.

    Args:
        request_id (int): ID of the book request to be approved.

    Returns:
        JSON response confirming the approval and issuance of the book.
    """
    book_request = BookRequest.query.get_or_404(request_id)
    book_request.status = "issued"
    user_book = UserBook(
        user_id=book_request.user_id,
        book_id=book_request.book_id,
        issued_date=datetime.now(),
        expiry_date=datetime.now() + timedelta(days=7),
    )
    db.session.add(user_book)
    db.session.commit()
    response_data = {
        "message": "Request approved and book issued successfully!",
        "status": "success",
    }
    return jsonify(response_data)


@api_bp.route("/request/deny/<int:request_id>", methods=["POST"])
@role_required("librarian")
def deny_request(request_id):
    """
    Deny a book request.

    Args:
        request_id (int): ID of the book request to be denied.

    Returns:
        JSON response confirming the denial of the request.
    """
    book_request = BookRequest.query.get_or_404(request_id)
    book_request.status = "denied"
    db.session.commit()
    response_data = {"message": "Request denied successfully!", "status": "success"}
    return jsonify(response_data)


@api_bp.route("/request/make/<int:book_id>", methods=["POST"])
@jwt_required()  # Ensure user is logged in
def request_book(book_id):
    """
    Request a book by its ID.

    Args:
        book_id (int): The ID of the book to request.

    Returns:
        tuple: A tuple containing JSON response and status code.
    """
    print("request_book function called")
    bk = Book.query.get_or_404(book_id)
    print(f"Book instance: {bk}")
    current_user = get_current_user()

    if current_user is None:
        abort(400, "No user")
    # Check if the user has already requested this book
    existing_request = BookRequest.query.filter_by(
        user_id=current_user.id, book_id=bk.book_id
    ).first()
    if existing_request:
        print("User has already requested this book")
        return jsonify({"message": "You have already requested this book."}), 400
    print(f"User ID: {current_user.id}, Book ID: {book_id}")
    # Create a new request for the book
    new_request = BookRequest(
        user_id=current_user.id, book_id=book_id, status="pending"
    )
    print(f"New request instance: {new_request}")
    db.session.add(new_request)
    print(str(new_request.query))
    db.session.commit()
    print("Changes committed to the database.")
    return jsonify({"message": "Book request submitted successfully."}), 200


@api_bp.route("/request/view")
@jwt_required()
def view_requests():
    """
    View all requests made by the current user.

    Returns:
        tuple: A tuple containing JSON response and status code.
    """
    current_user = get_current_user()

    if current_user is None:
        abort(400, "No user")
    else:
        user_requests = BookRequest.query.filter_by(user_id=current_user.id).all()
        requests_data = [
            {"book_name": req.book.book_name, "status": req.status}
            for req in user_requests
        ]
    return jsonify(requests_data), 200


# ---------------------------------------------- Stats APIs ------------------------------------------------------------------


# Endpoint for section distribution
@api_bp.route("/analytics/section-distribution")
def section_distribution():
    """Query section-wise book distribution"""
    section_distribution = (
        db.session.query(Section.section_name, db.func.count(Book.book_id))
        .join(Book, Section.section_id == Book.section_id)
        .group_by(Section.section_name)
        .all()
    )

    # Convert query result to JSON format
    distribution_data = [
        {"section_name": section_name, "book_count": book_count}
        for section_name, book_count in section_distribution
    ]

    return jsonify(distribution_data)


@api_bp.route("/analytics/user-login-activity")
@jwt_required()
def user_login_activity():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    # Query user login activity within the specified time period
    login_activity = User.query.filter(
        User.last_login.between(start_date, end_date)
    ).all()
    # Convert to dictionary format
    login_activity_data = [
        {
            "username": user.username,
            "login_time": user.last_login,
            "ip_address": user.last_ip,
        }
        for user in login_activity
    ]
    return jsonify(login_activity_data)


# API endpoint to get the counts
@api_bp.route("/book_requests/status_counts")
def get_status_counts():
    # Count the number of requests for each status
    issued_count = (
        db.session.query(func.count())
        .filter(BookRequest.status == "issued")
        .scalar()
    )
    denied_count = (
        db.session.query(func.count())
        .filter(BookRequest.status == "denied")
        .scalar()
    )
    pending_count = (
        db.session.query(func.count())
        .filter(BookRequest.status == "pending")
        .scalar()
    )

    # Return counts as JSON
    return jsonify(
        {
            "issued_count": issued_count,
            "denied_count": denied_count,
            "pending_count": pending_count,
        }
    )
