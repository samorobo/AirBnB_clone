#!/usr/bin/python3
"""This module defines class FileStorage that serializes instances to a JSON
file and deserializes JSON file to instances.
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """Represents a FileStorage class."""
    __file_path = "file.json"   # path to JSON file
    __objects = {}  # stores all objects with format - <class name>.id

    def all(self):
        """returns the object dictionary"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in `__objects` the object `obj`
        with key `<obj class name>.id`

        Args:
            obj (object): new FileStorage object
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """serializes `__objects` to JSON file."""
        to_dict = {}
        for key, obj in FileStorage.__objects.items():
            to_dict[key] = obj.to_dict()

        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(to_dict, f)

    def reload(self):
        """deserializes the JSON file to `__objects`."""
        try:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                _dict = json.load(f)

            new_dict = {}
            for obj_name, obj_details in _dict.items():
                _class = eval(obj_details["__class__"])
                obj = _class(**obj_details)
                new_dict[obj_name] = obj

            FileStorage.__objects = new_dict
        except FileNotFoundError:
            pass
