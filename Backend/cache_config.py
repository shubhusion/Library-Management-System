"""
Module for creating and configuring a Flask caching instance.
"""

from flask_caching import Cache


def make_cache(app):
    """
    Create and configure a Flask caching instance using Redis.

    This function configures the Flask application with Redis caching settings
    and creates a cache instance using Flask-Caching.

    Parameters:
        app (Flask): The Flask application instance.

    Returns:
        Cache: The configured cache instance.
    """
    app.config.from_mapping(
        {
            "CACHE_TYPE": "RedisCache",
            "CACHE_REDIS_HOST": "localhost",
            "CACHE_REDIS_PORT": 6379,
        }
    )  # Setting up Redis Cache

    cache = Cache(app)  # cache instance
    app.app_context().push()

    return cache
