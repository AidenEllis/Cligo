import time
from cligo.command import Command
from tests.utils.exceptions import Working
from cligo.exceptions import GotUnexpectedValueError, GotMultipleValueError, RequiredArgumentNotProvidedError


class TestNormalCommand(Command):
    permissions = []

    def process(self):
        time.sleep(0.3)
        a = 'Doing some stuffs'
        pass


class TestCommandRaiseWorking(Command):

    def process(self):
        time.sleep(0.3)
        raise Working()


class TestCommandCheckArgs(Command):

    def process(self, arg1, arg2):
        time.sleep(0.2)
        raise Working()

    def OnGotUnexpectedvalueError(self, command_name, value):
        raise GotUnexpectedValueError(None, None, None)

    def OnRequiredArgumentNotProvidedError(self, arg, command_obj):
        raise RequiredArgumentNotProvidedError(None, None)


class TestCommandCheckKwargs(Command):

    def process(self, arg1, arg2, defau="some default value"):
        if arg1 == 'value1' and arg2 == 'value2':
            raise Working()

    class Meta(Command.Meta):
        param_keywords = {
            'arg1': '-a1',
            'arg2': '-a2'
        }

    def OnGotMultipleValueError(self, command_name, arg_name):
        raise GotMultipleValueError(None, None, None)


class TestCommandNotASubclass:

    def process(self):
        pass


class TestCommandWithExtraKwargs(Command):

    def process(self, arg1, arg2, **kwargs):
        if kwargs:
            raise Working()

    class Meta(Command.Meta):
        kwarg_prefix = '-'
        param_keywords = {
            'arg1': '-a1',
            'arg2': '-a2'
        }


class TestCommandWithExtraArgs(Command):

    def process(self, arg1, arg2, *args):
        if args:
            raise Working()


class TestCommandWithExtraArgsAndKwargs(Command):

    def process(self, arg1, arg2, *args, **kwargs):
        if args and kwargs:
            raise Working()

    class Meta(Command.Meta):
        kwarg_prefix = '-'
        param_keywords = {
            'arg1': '-a1',
            'arg2': '-a2'
        }


class TestCommandCheckDefVal(Command):

    def process(self, arg1, arg2, defau="some default value"):
        if defau == "some default value" or defau == "defvalue":
            raise Working()

    class Meta(Command.Meta):
        param_keywords = {
            'arg1': '-a1',
            'arg2': '-a2',
            'defau': '-d'
        }


class TestCommandCheckOption(Command):

    def process(self, arg1, arg2="ABCD", *args, **kwargs):
        if self.request.options and self.request.options.opt1 and not self.request.options.someweirdoption:
            if arg1 and arg2 and args and kwargs:
                raise Working()

    class Meta(Command.Meta):
        kwarg_prefix = '-'
        param_keywords = {
            'arg1': '-a1',
            'arg2': '-a2'
        }
        option_prefix = '--'
