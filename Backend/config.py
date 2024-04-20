"""
    This module serves as the Configuration Settings for the application
"""

class Config(object):
    """
    Base configuration class.
    
    Attributes:
        DEBUG (bool): Flag for debugging mode.
        TESTING (bool): Flag for testing mode.
    """
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """
    Configuration class for development environment.
    
    Inherits from Config class.
    
    Attributes:
        DEBUG (bool): Flag for debugging mode (set to True).
        SQLALCHEMY_DATABASE_URI (str): URI for the development database.
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.sqlite3'
    JWT_SECRET_KEY = '5eb98d6cf22342f63cab91e9'
