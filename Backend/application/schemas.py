"""
Module for Defining Output Schemas
"""

from marshmallow import fields, Schema

class UserSchema(Schema):
    """
    User Schema
    """
    id = fields.Integer()
    username = fields.String()
    email = fields.String()
    role_id = fields.String()
