""" Module for Starting point of Application """

from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
from application.models import db, Role, TokenBlocklist, User , Section
from application.controllers import api_bp, jwt
from config import DevelopmentConfig
from celery_config import make_celery
from cache_config import make_cache
from werkzeug.security import generate_password_hash
import requests


def create_app():
    """Create and configure the Flask app instance.
    Returns:
        Flask: The configured Flask app instance.
    """
    ap = Flask(__name__)
    ap.config.from_object(DevelopmentConfig)
    CORS(
        ap,
        resources={r"/*": {"origins": "http://localhost:8080"}},
        supports_credentials=True,
    )

    with ap.app_context():
        db.init_app(ap)
        jwt.init_app(ap)
        db.create_all()
        role_admin = Role(id="admin", name="admin", description="Admin Description")
        db.session.add(role_admin)
        role_libra = Role(
            id="libra", name="librarian", description="Librarian Description"
        )
        db.session.add(role_libra)
        role_user = Role(id="user", name="user", description="user Description")
        db.session.add(role_user)

        
        user_libra = User(username="shubham2703", email="shubham@gmail.com", password="shubham", role_id="librarian")
        db.session.add(user_libra)
        user_user = User(username="shivam", email="shivam@gmail.com", password="shivam", role_id="user")
        db.session.add(user_user)
        fiction = Section(section_name="Fiction",description = " Fiction")
        db.session.add(fiction)
        nonfiction = Section(section_name="Non-Fiction",description = " Non -Fiction")
        db.session.add(nonfiction)
        ap.register_blueprint(api_bp, url_prefix="/api")

        ### load user
        @jwt.user_lookup_loader
        def user_lookup_callback(_jwt_headers, jwt_data):
            identity = jwt_data["sub"]
            return User.query.filter_by(username=identity).one_or_none()

        @jwt.expired_token_loader
        def expired_token_callback(jwt_header, jwt_data):
            return jsonify({"message": "Token has expired", "error": "Token Expired"})

        @jwt.invalid_token_loader
        def invalid_token_callback(error):
            return jsonify(
                {"message": "Signature Verification Failed", "error": "Invalid Token"}
            )

        @jwt.unauthorized_loader
        def missing_token_callback(error):
            return jsonify(
                {
                    "message": "Request Does not Contain valid token",
                    "error": "authorisation_header",
                }
            )

        @jwt.token_in_blocklist_loader
        def token_in_blocklist_callback(jwt_header, jwt_data):
            jti = jwt_data["jti"]
            token = (
                db.session.query(TokenBlocklist)
                .filter(TokenBlocklist.jti == jti)
                .scalar()
            )
            return token is not None

        try:
            db.session.commit()
        except:
            pass

    return ap


app = create_app()
cache = make_cache(app)
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
app.config["CELERY_BACKEND"] = "redis://localhost:6379/0"
celery = make_celery(app)

if __name__ == "__main__":
    app.run(debug=True)

    # # Add some initial users via API call
    # initial_users = [
    #     {
    #         "username": "john_doe",
    #         "email": "john@example.com",
    #         "password": "password123",
    #         "role_id": "user",
    #     },
    #     {
    #         "username": "jane_smith",
    #         "email": "jane@example.com",
    #         "password": "password456",
    #         "role_id": "libra",
    #     },
    # ]

    # for user_data in initial_users:
    #     response = requests.post("http://127.0.0.1:5000/api/register", json=user_data)
    #     if response.status_code == 201:
    #         print(f"User '{user_data['username']}' created successfully")
    #     else:
    #         print(f"Failed to create user '{user_data['username']}': {response.json()}")
