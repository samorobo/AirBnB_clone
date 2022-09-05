#!/usr/bin/python3
"""This module defines a class User."""
from .base_model import BaseModel


class User(BaseModel):
    """Represents call User that inherits from BaseModel."""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
