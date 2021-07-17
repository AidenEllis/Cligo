import sys
from commands import commandManager


def execute_from_command_line():
    args = sys.argv[1:]
    commandManager(args)


execute_from_command_line()
