from tests.base import CliGoTestCase
from tests.utils import commands, permissions, exceptions


class TestCliPermissions(CliGoTestCase):

    def test_registered_permissions(self):
        """
        Checks if permission is registered
        """
        the_command = commands.TestNormalCommand

        the_command.permissions = [permissions.TestPermissionTrue]
        self.app.register(the_command, command_name='test')
        self.app.run_from_terminal("python main.py test")

        self.assertTrue(self.app.commands['test']['permissions'])

    def test_check_permission_granted_working(self):
        """
        Checks if permission granted works
        """
        the_command = commands.TestCommandRaiseWorking

        the_command.permissions = [permissions.TestPermissionTrue]
        self.app.register(the_command, command_name='test')

        with self.assertRaises(exceptions.Working):
            self.app.run_from_terminal("python main.py test")

    def test_check_permission_denied_working(self):
        """
        Checks if permission denied is working
        """
        the_command = commands.TestNormalCommand

        the_command.permissions = [permissions.TestPermissionFalse]
        self.app.register(the_command, command_name='test')

        with self.assertRaises(exceptions.PermissionDenied):
            self.app.run_from_terminal("python main.py test")

    def test_multiple_permission_granted_working(self):
        """
        Registers multiple permission and sees if granted works
        """
        the_command = commands.TestCommandRaiseWorking

        the_command.permissions = [
            permissions.TestPermissionTrue,
            permissions.TestPermissionTrue,
            permissions.TestPermissionTrue
        ]
        self.app.register(the_command, command_name='test')

        with self.assertRaises(exceptions.Working):
            self.app.run_from_terminal("python main.py test")

    def test_multiple_permission_denied_working(self):
        """
        Registers multiple permission and checks if denied works
        """
        the_command = commands.TestNormalCommand

        the_command.permissions = [
            permissions.TestPermissionFalse,
            permissions.TestPermissionFalse
        ]
        self.app.register(the_command, command_name='test')

        with self.assertRaises(exceptions.PermissionDenied):
            self.app.run_from_terminal("python main.py test")

    def test_permission_mixed_type_1(self):
        """
        Mixed type of registered permission which checks permission denies at
        TestPermissionFlaseDummyFalse
        """
        the_command = commands.TestNormalCommand

        the_command.permissions = [
            permissions.TestPermissionTrue,
            permissions.TestPermissionFlaseDummyFalse,
            permissions.TestPermissionTrue,
        ]

        self.app.register(the_command, command_name='test')

        with self.assertRaises(exceptions.DummyFalse):
            self.app.run_from_terminal("python main.py test")

    def test_permission_mixed_type_2(self):
        """
        Checks if permissions passes TestPermissionRaisesWorking
        """
        the_command = commands.TestNormalCommand

        the_command.permissions = [
            permissions.TestPermissionTrue,
            permissions.TestPermissionTrue,
            permissions.TestPermissionRaisesWorking
        ]

        self.app.register(the_command, command_name='test')

        with self.assertRaises(exceptions.Working):
            self.app.run_from_terminal("python main.py test")
