#!/usr/bin/python3

import cmd
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
import re
from models.base_model import BaseModel
from models import storage
from models.user import User

class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb)"
    model_list = ["Basemodel", "User", "City", "State", "Place", "Amenity", "Review"]

    str_dict = None

    def precmd(self, line):
        if '.' in line:
            if '{' in line:
                dict_ = re.search("{([^}]*)}", line).group(0)
                HBNBCommand.str_dict = eval(dict_)
                pass

            line_arg = line.replace('.', ' ').replace(', ', ' ').replace('(', ' ').replace(')', ' ')

            line_arg = line_arg.split()
            line_arg[0], line_arg[1] = line_arg[1], line_arg[0]
            line = ' '.join(line_arg)
        return cmd.Cmd().precmd(line)

    def do_quit(self, args):
        """
        This is command quits the interpreter
        """
        return True

    def do_EOF(self, args):
        """
        This command quits the interpreter
        """
        return True

    def emptyline(self):
        return False

    def onecmd(self, args):
        if args == "quit":
            return self.do_quit(args)
        elif args == "EOF":
            return self.do_EOF(args)
        else:
            cmd.Cmd.onecmd(self, args)

    @classmethod
    def handle_errors(cls, args, **kwargs):
        if all in kwargs.value():
            if not args:
                return False

        if not args:
            print("** class name missing **")
            return True
        else:
            args = args.split(" ") #args becomes a list

            n = len(args)
            if args[0] not in HBNBCommand.model_list:
                print("** class doesn't exist **")
                return True

            if 'com' not in kwargs:
                return False

            for arg in kwargs.values():
                if arg in ["show", "destroy"]:
                    if n < 2:
                        print("** instance id missing **")
                        return True

                if arg == "update":
                    if n < 2:
                        print("** instance id missing **")
                        return True
                    elif n < 3:
                        print("** attribute name missing **")
                        return True
                    elif n < 4:
                        print("** value missing **")
                        return True

            return False



    def do_create(self, args):
        error = HBNBCommand.handle_errors(args)

        if error:
            return

        obj = eval(args)()
        obj.save()
        print(obj.id)

    def do_show(self, args):
        error = HBNBCommand.handle_errors(args, command="show")
        if error:
            return

        args = args.split(" ")

        objects = storage.all()
        key = ".".join(args)
        obj = objects.get(key)
        if obj:
            print(obj)
        else:
            print("** instance id missing **")

    def do_destroy(self, args):
        error = HBNBCommand.handle_errors(args, com="destroy")
        if error:
            return

        args = args.split()
        key = f"{args[0]}.{args[1]}"
        objects = storage.all()

        if key in objects and storage.delete(objects[key]):
            pass
        else:
            print("** instance id not found **")

    def do_all(self, args):
        error = HBNBCommand.handle_errors(args, com="all")

        if error:
            return

        args = args.split(" ")

        objects = storage.all()

        if args[0] == "":
            for obj in objects.value:
                print(obj)
        else:
            for key in objects:
                k = key.split(".")
                if key[0] == args[0]:
                    print(objects[key])



    def do_update(self, args):
        error = HBNBCommand.handle_errors(args, com="update")

        if error:
            return

        args = args.split()
        class_name = args[0]
        id = args[1]
        attr_name = args[2]
        attr_value = args[3]

        if "\"" in attr_value:
            atrr_value = attr_value[1:-1]


        if attr_value.isdigit():
            attr_value = int(attr_value)

        objects = storage.all()
        key = f"{class_name}.{id}"

        for k in objects:
            if k == key:
                obj = objects[k]
                setattr(obj, attr_name, attr_value)
                obj.save()
                return

        print("** instance id not found **")


if __name__=="__main__":
    HBNBCommand().cmdloop
