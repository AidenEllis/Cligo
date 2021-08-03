from tests.base import CliGoTestCase
from tests.utils import commands, exceptions


class CliGeneralTest(CliGoTestCase):

    def test_check_args_working(self):
        """Check if command is working with args"""
        the_command = commands.TestCommandCheckArgs
        self.app.register(the_command, command_name='test')

        with self.assertRaises(exceptions.Working):
            self.app.run_from_terminal("python main.py test arg1 arg2")

    def test_check_kwargs_working(self):
        """Check if command is working with kwargs"""
        the_command = commands.TestCommandCheckKwargs
        self.app.register(the_command, command_name='test')

        with self.assertRaises(exceptions.Working):
            self.app.run_from_terminal("python main.py test -a1 value1 -a2 value2")

        with self.assertRaises(exceptions.Working):
            self.app.run_from_terminal("python main.py test -a2 value2 -a1 value1")

    def test_check_mixed_arg_kwargs_working(self):
        """Check if command is working with both arg and kwarg"""
        the_command = commands.TestCommandCheckKwargs
        self.app.register(the_command, command_name='test')

        with self.assertRaises(exceptions.Working):
            self.app.run_from_terminal("python main.py test value1 -a2 value2")

    def test_check_extra_kwargs_working(self):
        """Check if extra keyword is working"""
        the_command = commands.TestCommandWithExtraKwargs
        self.app.register(the_command, command_name='test')

        with self.assertRaises(exceptions.Working):
            self.app.run_from_terminal("python main.py test value1 -a2 value2 -e1 extra1 -e2 extra2")

        with self.assertRaises(exceptions.Working):
            self.app.run_from_terminal("python main.py test -a1 value1 -a2 value2 -e1 extra1 -e2 extra2")

    def test_check_extra_args_working(self):
        """Check if extra args is working"""
        the_command = commands.TestCommandWithExtraArgs
        self.app.register(the_command, command_name='test')

        with self.assertRaises(exceptions.Working):
            self.app.run_from_terminal("python main.py test value1 value2 extra1 extra2")

    def test_check_both_extra_args_and_kwargs(self):
        """Check both extra args and kwargs are working"""
        the_command = commands.TestCommandWithExtraArgsAndKwargs
        self.app.register(the_command, command_name='test')

        with self.assertRaises(exceptions.Working):
            self.app.run_from_terminal("python main.py test value1 value2 Earg1 Earg2 Earg3 -e1 ekwrg1 -e2 ekwrg2")

    def test_check_default_value_is_working(self):
        """Check if default value is working with args and kwargs"""
        the_command = commands.TestCommandCheckDefVal
        self.app.register(the_command, command_name='test')

        with self.assertRaises(exceptions.Working):
            self.app.run_from_terminal("python main.py test argval1 argval2 defvalue")

        with self.assertRaises(exceptions.Working):
            self.app.run_from_terminal("python main.py test argval1 -a2 argval2 -d defvalue")

    def test_check_option_feature(self):
        the_command = commands.TestCommandCheckOption

        self.app.register(the_command, command_name='test')

        with self.assertRaises(exceptions.Working):
            self.app.run_from_terminal("python main.py test argval1 brrr addArg1 addArg2 -addKwarg val123 --opt1")
