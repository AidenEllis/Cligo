from cligo.exceptions import *
from tests.base import CliGoTestCase
from tests.utils import commands, errors


class CliExceptionsTest(CliGoTestCase):

    def test_check_extra_args_error_working(self):
        """
        Checks if command throws error on using extra args if extra args is disabled
        """
        the_command = commands.TestCommandCheckArgs
        self.app.register(the_command, command_name='test')

        with self.assertRaises(GotUnexpectedValueError):
            self.app.run_from_terminal("python main.py test arg1 arg2 arg3")

    def test_check_multiple_value_error_arg_after_kwarg(self):
        """Check if it throws error when using arg after kwarg"""
        the_command = commands.TestCommandCheckKwargs
        self.app.register(the_command, command_name='test')

        with self.assertRaises(GotMultipleValueError):
            self.app.run_from_terminal("python main.py test -a1 value1 value2")

    def test_check_required_argument_not_provided_error(self):
        """Check if commands throws error when required argument is not provided"""
        the_command = commands.TestCommandCheckArgs
        self.app.register(the_command, command_name='test')

        with self.assertRaises(RequiredArgumentNotProvidedError):
            self.app.run_from_terminal("python main.py test")

        with self.assertRaises(RequiredArgumentNotProvidedError):
            self.app.run_from_terminal("python main.py test arg1")

    def test_check_command_not_found_error(self):
        """Check if it throws an error when theres no command name it called"""
        self.app.register(commands.TestNormalCommand, command_name='test')
        self.app.set_on_command_not_found_error(errors.OnCommandNotFoundError)

        with self.assertRaises(CommandNotFoundError):
            self.app.run_from_terminal("python main.py someweirdname")

    def test_check_command_not_a_command_subclass_error(self):
        """
        Checks if the command class is inherited from cligo.command.Command else throw an error
        """
        with self.assertRaises(NotACommandSubClassError):
            self.app.register(commands.TestCommandNotASubclass, command_name='test')
