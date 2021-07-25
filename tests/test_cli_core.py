from tests.base import CliGoTestCase
from tests.utils import commands, exceptions


class CliCoreTest(CliGoTestCase):

    def test_check_registered_commands(self):
        """
        Checks if command is registered.
        """
        self.app.register(commands.TestNormalCommand, command_name='test')
        self.app.run_from_terminal("python main.py test")

        self.assertTrue(self.app.commands)

    def test_check_command_process_method_working(self):
        """
        Checks if COmmand.process method is responding / working.
        """
        self.app.register(commands.TestCommandRaiseWorking, command_name='test')

        with self.assertRaises(exceptions.Working):
            self.app.run_from_terminal("python main.py test")
