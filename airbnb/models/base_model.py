#!/usr/bin/python3
"""This module defines class BaseModel and all it's attributes/methods."""
import uuid
from datetime import datetime
import models


class BaseModel:
    """Represents a class BaseModel."""
    def __init__(self, *args, **kwargs):
        """Instantiates a BaseModel class instance,
        with the following public attributes:

        Attr_1:
            id - Unique ID for each BaseModel instance
            created_at - Current datetime the instance is created
            updated_at - Current datetime when instance is created,
                        and to updated every time object is changed
        """
        if kwargs:
            for key in kwargs.keys():
                if key != '__class__':
                    if key in ['created_at', 'updated_at']:
                        value = datetime.fromisoformat(kwargs[key])
                        self.__setattr__(key, value)
                    else:
                        self.__setattr__(key, kwargs[key])
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """returns the string representation of BaseModel instance.
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """updates the instance attribute `updated_at` with current datetime.
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """returns a dictionary representation of the BaseModel instance.
        """
        to_dict = self.__dict__.copy()
        to_dict["__class__"] = self.__class__.__name__
        to_dict["created_at"] = self.created_at.isoformat()
        to_dict["updated_at"] = self.updated_at.isoformat()
        return to_dict
        dct = self.__dict__.copy()
        dct["updated_at"] = self.updated_at.isoformat()
        dct["created_at"] = self.created_at.isoformat()
        dct["__class__"] = type(self).__name__
        return dct

    def __str__(self):
        """returns the string representation of the class 'BaseModel'"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
