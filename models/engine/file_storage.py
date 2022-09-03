#!/usr/bin/python3

'''file_storage.py
'''

import json
from models.base_model import BaseModel
from models.user import User


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        return FileStorage.__objects

    def new(self, obj):
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        to_dict = {}
        for key, obj in FileStorage.__objects.items():
            to_dict[key] = obj.to_dict()

        with open(FileStorage.__file_path, "w") as f:
            json.dump(to_dict, f, indent=4)

    def reload(self):
        try:
            with open(FileStorage.__file_path, "r") as f:
                _dict = json.load(f)

            new_dict = {}
            for obj_name, obj_details in _dict.items():
                class_name = obj_name.split(".")[0]
                obj = eval(class_name)(**obj_details)
                new_dict[obj_name] = obj

            FileStorage.__objects = new_dict
        except FileNotFoundError:
            pass

    def delete(self, obj):
        class_name = obj.__class__.__name__
        id = obj.id
        key = f"{class_name}.{id}"

        if key in FileStorage.__objects:
            del FileStorage.__objects[key]
            self.save()
            return True

        return False
