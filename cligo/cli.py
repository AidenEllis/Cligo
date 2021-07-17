from cligo import process
from cligo.exceptions import CommandNotFound


class CliApp:
    def __init__(self, name: str):
        self.name = name
        self.commands = process.commands

    @staticmethod
    def register(func, command_name, permissions: list = None):
        permissions = [] if not permissions else permissions
        process.commands[command_name] = {
            'command': func,
            'permissions': permissions
        }

    def execute(self, args):
        command = args[0]

        if command in self.commands:
            command_obj = self.commands[command]
            context = {}
            if command_obj['permissions']:
                for permission in command_obj['permissions']:
                    # Loops through all the given permissions, continue the process if permission granted
                    # otherwise, run on_permission_denied()

                    has_permission = permission().process(request=context)
                    if not has_permission:
                        permission().on_permission_denied(request=context)
                        return
                    else:
                        pass

            context = {}
            return command_obj['command'](request=context)
        else:
            raise CommandNotFound(command)

    def run(self, args):
        try:
            args = args[1:]
            self.execute(args)

        except CommandNotFound as e:
            print(e)
