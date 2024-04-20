from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_current_user
from flask_jwt_extended import verify_jwt_in_request , jwt_required
from application.models import User, Role

def role_required(role_id):
    """
    Decorator function that checks if the current user has the specified role.

    Args:
        role_id (str): The ID of the role that is required.

    Returns:
        function: A decorator function that wraps the original function.
    """
    @jwt_required
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            """
            Wrapper function that checks the role of the current user.

            Args:
                *args: Arbitrary positional arguments.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                JSON response: Returns an error message if the user does not have the required role.
                Otherwise, returns the result of the original function.
            """
            
            current_user = get_current_user()

            user = User.query.get(current_user)
            if user is None:
                return jsonify({"message": "User not found"}), 404
            if user.role_id != role_id:
                return jsonify({"message": "Unauthorized access"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator