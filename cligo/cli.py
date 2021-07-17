from .decorators import parametrized
from .process import commands


class CliApp:
    def __init__(self, name: str):
        self.name = name
        self.commands = commands

    @staticmethod
    @parametrized
    def register(func, command_name: str):
        commands.append({command_name: func})

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
