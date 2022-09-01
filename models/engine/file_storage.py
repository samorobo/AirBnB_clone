from models.base_model import BaseModel
import json


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        return FileStorage.__objects

    def new(self, obj):
        key = f"{obj.__class__.name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        to_dict = {}
        for key, obj in FileStorage.__objects.items():
            to_dict[key] = obj.to_dict

        with open(FileStorage.__file_path, "w") as f:
            json.dump(to_dict, f)

    def reload(self):
        try:
            with open(FileStorage.__file_path, 'r') as file:
                dict = json.load(file)

                new_dict = {}
                for obj_name, obj_details in dict.items():
                    obj = BaseModel(**obj_details)
                    new_dict[obj_name] = obj

                FileStorage.__object = new_dict
        except FileNotFoundError:
            pass
