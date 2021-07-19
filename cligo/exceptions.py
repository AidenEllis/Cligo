class CommandNotFoundError(Exception):
    __module__ = Exception.__module__

    def __init__(self, command_name):
        message = f"Command {command_name} not found."
        self.message = message
        self.command_name = command_name
        super().__init__(self.message)


class GotUnexpectedValueError(Exception):
    __module__ = Exception.__module__

    def __init__(self, command_obj, command_name, value):
        message = f"Command <{command_name}> got unexpected value '{value}'"
        self.message = message
        self.command_name = command_name
        self.value = value
        self.command_obj = command_obj
        super().__init__(self.message)


class GotMultipleValueError(Exception):
    __module__ = Exception.__module__

    def __init__(self, command_obj, command_name, arg_name):
        message = f"Command <{command_name}> got multiple values for argument '{arg_name}'"
        self.message = message
        self.command_name = command_name
        self.arg_name = arg_name
        self.command_obj = command_obj
        super().__init__(self.message)


class NotACommandSubClassError(Exception):
    __module__ = Exception.__module__

    def __init__(self, class_name):
        message = f"Class {class_name} is not a subclass of cligo.command.Command"
        self.message = message
        super().__init__(self.message)


class RequiredArgumentNotProvidedError(Exception):
    __module__ = Exception.__module__

    def __init__(self, required_arg, command_obj):
        message = f"Required argument <{required_arg}> not provided, class: <{command_obj}>"
        self.message = message
        self.required_arg = required_arg
        self.command_obj = command_obj
        super().__init__(self.message)
