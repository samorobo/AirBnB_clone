#!/usr/bin/python3
"""This module the defines the entry point
for the console command interpreter.
"""
import cmd
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class HBNBComand(cmd.Cmd):
    """Defines the HBNBCommand class for console implemantation."""
    prompt = "(hbnb) "

    class_model = (
        "BaseModel",
        "User",
        "City",
        "State",
        "Place",
        "Amenity",
        "Review"
        )

    str_dict = None

    @classmethod
    def striped(cls, arg):
        """Strips `arg` string of first and last character. """
        return arg[1:-1]

    def precmd(self, line):
        """Strips the line input before interpreted by `onecmd`."""
        if '.' in line:
            if '{' in line:
                dict_ = re.search("{([^}]*)}", line)
                if not dict_:
                    return cmd.Cmd().precmd(line)
                dict_ = dict_.group(0)
                HBNBComand.str_dict = eval(dict_)
                pass

            line_arg = line.replace('.', ' ').replace(', ', ' ')\
                .replace('(', ' ').replace(')', ' ')

            line_arg = line_arg.split()
            line_arg[0], line_arg[1] = line_arg[1], line_arg[0]
            if len(line_arg) > 2:
                if "\"" in line_arg[2]:
                    line_arg[2] = HBNBComand.striped(line_arg[2])
            line = ' '.join(line_arg)

        return cmd.Cmd().precmd(line)

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        return True

    @classmethod
    def HBNBError(cls, line, command=None):
        """Defines error handler method for HBNBCommand."""
        args = line.split()
        if not args:
            print("** class name missing **")
            return True
        if args[0] not in HBNBComand.class_model:
            print("** class doesn't exist **")
            return True
        if len(args) < 2 and command not in ('create', 'all', 'count'):
            print("** instance id missing **")
            return True

        if command in ("show", "delete", "update"):
            obj = storage.all()
            key = f"{args[0]}.{args[1]}"
            _str = obj.get(key)
            if _str is None:
                print("** no instance found **")
                return True

        return False

    def do_create(self, line):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        args = line.split()
        if HBNBComand.HBNBError(line, "create"):
            return

        class_ = eval(args[0])
        obj_ = class_()
        print(obj_.__dict__["id"])
        storage.save()

    def do_show(self, line):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        args = line.split()
        if HBNBComand.HBNBError(line, "show"):
            return

        obj_dict = storage.all()
        key = f"{args[0]}.{args[1]}"
        _str = obj_dict.get(key)
        print(_str)

    def do_destroy(self, line):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        args = line.split()
        if HBNBComand.HBNBError(line,  "delete"):
            return
        key = f"{args[0]}.{args[1]}"
        obj = storage.all()
        del (obj[key])
        storage.save()

    def do_all(self, line):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        args = line.split()
        _str = []
        obj = storage.all()

        if args:
            if HBNBComand.HBNBError(line, 'all'):
                return
            key = args[0]
            for item in obj:
                if key in item:
                    _str.append(str(obj.get(item)))

        else:
            for item in obj:
                _str.append(str(obj.get(item)))
        ", ".join(_str)
        print(_str)

    def do_update(self, line):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        args = line.split()

        if HBNBComand.HBNBError(line, "update"):
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return

        obj_dict = storage.all()
        key = f"{args[0]}.{args[1]}"
        item = obj_dict.get(key)

        if HBNBComand.str_dict:
            for key in HBNBComand.str_dict:
                value = HBNBComand.str_dict[key]
                setattr(item, key, value)
            HBNBComand.str_dict = None
        else:
            setattr(item, args[2], args[3])
        item.save()
        storage.save()

    def do_count(self, line):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        if HBNBComand.HBNBError(line, "count"):
            return
        count = 0
        args = line.split()
        obj = storage.all()

        key = args[0]
        for item in obj:
            if key in item:
                count += 1
        print(count)
        storage.save()

    def emptyline(self):
        """Do nothing if empty line is passed."""
        pass


if __name__ == "__main__":
    HBNBComand().cmdloop()
