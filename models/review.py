#!/usr/bin/python3
"""This module defines a class Review."""
from .base_model import BaseModel


class Review(BaseModel):
    """Represents a class for Review instances."""
    place_id = ""
    user_id = ""
    text = ""
