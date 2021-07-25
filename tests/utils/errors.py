from cligo.core.error import CliError
from cligo.exceptions import CommandNotFoundError


class OnCommandNotFoundError(CliError):

    def on_error(self, command_name):
        raise CommandNotFoundError(command_name)
