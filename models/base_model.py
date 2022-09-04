#!/usr/bin/python3

import uuid
from datetime import datetime 
import models

class BaseModel:
    def __init__(self, *args, **kwargs):

        tformat = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        models.storage.new(self)

        if len(kwargs) != 0:
            for key, value in kwargs.items:
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(value, tformat)
                else:
                    self.__dict__[key] = value

    def save(self):
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        to_dict = self.__dict__.copy
        to_dict['__class__'] = self.__class__.__name__
        to_dict['created_at'] = self.created_at.isoformat()
        to_dict['updated_at'] = self.updated_at.isoformat()

        return to_dict

    def __str__(self):
        clname = self.__class__.__name__
        return "[{}] ({}) {}".format(clname, self.id, self.__dict__)
