#!/usr/bin/python3
"""This module defines a class City."""
from .base_model import BaseModel


class City(BaseModel):
    """Represents a City class that inherits BaseModel."""
    state_id = ""
    name = ""
