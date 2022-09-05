#!/usr/bin/python3
"""a program called 'console.py' that contains the entry
point of the command interpreter """
import cmd
from models.base_model import BaseModel
from models import storage
from models.engine.file_storage import FileStorage
from models.user import User
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.amenity import Amenity


class HBNBCommand(cmd.Cmd):
    """cmd class 'HBNBCommand(cmd.Cmd)' """
    prompt = "(hbnb) "

    class_list = ["BaseModel", "Amenity", "User", "City", "Place",
                  "Review", "State"]

    def precmd(self, line):
        """When precmd() is called, the 'line' is stripped of [, . ()"] then
        joined and passed to the interpreter"""
        if "." in line:
            line_arg = line.replace('.', ' ').replace(',', ' ')\
                .replace('(', ' ').replace('"', '').replace(')', ' ')
            line_arg = line_arg.split()
            line_arg[0], line_arg[1] = line_arg[1], line_arg[0]
            line = " ".join(line_arg)
        return cmd.Cmd().precmd(line)

    def do_quit(self, line):
        """Quit command to exit the program\n"""
        return True

    def do_EOF(self, line):
        """Quit command to exit the program\n"""
        return True

    def emptyline(self):
        """prevents executing last command when enter
        is pressed without a new command/argument"""
        pass

    @classmethod
    def error_handler(cls, line, **kwargs):
        """Handling all errors in HBNBCommand class"""
        if "all" in kwargs.values():
            if not line:
                return False
        if not line:
            print("** class name missing **")
            return True
        else:
            args = line.split(" ")

        if args[0] not in HBNBCommand.class_list:
            print("** class doesn't exist **")
            return True

        n = len(args)
        if "command" not in kwargs:
            return False
        for arg in kwargs.values():
            if arg in ["show", "destroy", "update"]:
                if n < 2:
                    print("** instance id missing **")
                    return True
            if arg == "update":
                if n < 3:
                    print("** attribute name missing **")
                    return True
                elif n < 4:
                    print("** value missing **")
                    return True
        return False

    def do_create(self, line):
        """Creates a new instance of the class and saves
        it (to the JSON file) and prints the id"""
        err = HBNBCommand.error_handler(line)
        if err:
            return
        my = eval(line)()
        my.save()
        print(my.id)

    def do_show(self, line):
        """prints the string representation of an instance
        based on the class name and id"""
        err = HBNBCommand.error_handler(line, command="show")
        if err:
            return
        arg = line.split(" ")
        key = f"{arg[0]}.{arg[1]}"
        store = storage.all()
        obj = store.get(key)
        if obj:
            print(obj)
        else:
            print("** no instance found **")

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id
        (save the change into the JSON file)"""
        err = HBNBCommand.error_handler(line, command="destroy")
        if err:
            return
        else:
            arg = line.split(" ")
            key = ".".join(arg)
            store = storage.all()
            if key in store:
                del storage.all()[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, line):
        """ prints all string representations of all instances
        based on or not the class name and id """

        err = HBNBCommand.error_handler(line, command="all")
        if err:
            return

        args = line.split(" ")
        objects = storage.all()
        if args[0] == "":
            for obj in objects.values():
                print(obj)

        else:
            for key in objects:
                k = key.split(".")
                if k[0] == args[0]:
                    print(objects[key])

    def do_count(self, line):
        """ counts the number of instances of the class passed: 'line'"""
        arg = line.split(" ")
        store = storage.all()
        count = 0

        if len(arg) > 0 and arg[0] not in HBNBCommand.class_list:
            print("** class doesn't exist **")
        else:
            key = arg[0]
            for item in store:
                if key in item:
                    count += 1
            print(count)

    def do_update(self, line):
        """ Updates an instance based on the class name and
        id by adding or updating attribute (save the change
        into the JSON file). """
        err = HBNBCommand.error_handler(line, command="update")
        if err:
            return
        args = line.split()
        store = storage.all()
        key = "{}.{}".format(args[0], args[1])
        arg3 = args[3]
        arg2 = args[2]
        arg2 = arg2.strip('"')
        arg2 = arg2.strip("'")
        if (arg3).isdigit():
            arg3 = int(arg3)
        else:
            arg3 = arg3.strip('"')
            arg3 = arg3.strip("'")
        for k in store:
            if k == key:
                setattr(store[key], arg2, arg3)
                store[key].save()
                return
        print("** instance not found **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
