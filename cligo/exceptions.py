class CommandNotFound(Exception):
    __module__ = Exception.__module__

    def __init__(self, command_name):
        message = f"Command {command_name} not found."
        self.message = message
        super().__init__(self.message)
