#!/usr/bin/python3
"""Defines the class: BaseModel"""
from datetime import datetime as dt
import uuid
import models


class BaseModel:
    """The BaseModel class"""

    def __init__(self, *args, **kwargs):
        """initialization of basemodel.
        Args: *args - Unused
            **kwargs (dict) - pair of attributes"""
        if kwargs:
            for key in kwargs.keys():
                if key != "__class__":
                    if key in ["created_at", "updated_at"]:
                        self.__dict__[key] = dt.fromisoformat(kwargs[key])
                    else:
                        self.__dict__[key] = kwargs[key]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = dt.now()
            self.updated_at = dt.now()
            models.storage.new(self)

    def save(self):
        """updates the public instance attribute 'updated_at' with the
        current datetime"""
        self.updated_at = dt.now()
        models.storage.save()

    def to_dict(self):
        """returns a dictionary representation of BaseModel"""
        dct = self.__dict__.copy()
        dct["updated_at"] = self.updated_at.isoformat()
        dct["created_at"] = self.created_at.isoformat()
        dct["__class__"] = type(self).__name__
        return dct

    def __str__(self):
        """returns the string representation of the class 'BaseModel'"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
