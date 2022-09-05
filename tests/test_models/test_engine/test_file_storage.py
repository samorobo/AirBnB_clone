#!/usr/bin/python3
"""Defines the class: FileStorage"""
import json
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.amenity import Amenity


class FileStorage:
    """The FileStorage class serialises instances of JSON file
    and deserialises JSON files to instances """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the class attribute (dictionary): __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects, the obj with key '<obj class name>.id"""
        FileStorage.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path"""
        json_objects = {}
        for key, value in FileStorage.__objects.items():
            json_objects[key] = value.to_dict()
        with open(FileStorage.__file_path, "w") as f:
            json.dump(json_objects, f, indent=4)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        try:
            with open(FileStorage.__file_path, "r") as f:
                diction = json.load(f)

            new_dcti = {}
            for key, value in diction.items():
                ki = key.split(".")[0]
                obj = eval(ki)(**value)
                new_dcti[key] = obj

            FileStorage.__objects = new_dcti

        except FileNotFoundError:
            pass
