import sys
import typing
from cligo import process
from cligo.exceptions import *
from .utils.funcTools import *
from cligo.command import Command
from cligo.core.error import CliError
from .db.manager import DBManager


__all__ = ['CliApp']


class CliApp:

    configuration = {}

    def __init__(self, name: str):
        self.name = name
        self.commands = process.commands
        self.on_command_not_found_error = None
        self.db = DBManager(CliApp.configuration.get('database'))

    @staticmethod
    def config(database=None):
        """
        sets configuration for the class, as a dict.
        """
        CliApp.configuration['database'] = database

    @staticmethod
    def register(command_obj: typing.Type[Command], command_name: str):
        """
        Adds the command process & its permissions to process.commands dict.
        commands dict blueprint:
            commands = {
                'someCommandName': {
                    'command': <The command class object 0x0000>
                    'permissions': [<permissions class objects 0x0000>]
                }
            }
        Before adding we check if the command_obj is inherited from command.Command class
        """

        if not issubclass(command_obj, Command):
            raise NotACommandSubClassError(command_obj.__name__)

        process.commands[command_name] = {
            'command': command_obj,
            'permissions': command_obj.permissions  # command_obj.permissions is a list
        }

    def execute(self, prams: list):
        """
        Handles the command object, implements permissions, checks for errors,
        handles input parameters (arg, kwarg)
        """

        command_name = prams[0]
        input_prams = prams[1:]  # removes the command name from list

        args = list(input_prams)
        kwargs = {}

        if command_name in self.commands:
            command_dict = self.commands[command_name]
            command_obj = command_dict['command']()  # Inititlizing class with ()

            # parameters of the func / method
            func_params = get_func_args(func=command_obj.process, remove_vals=['*args', '**kwargs'])[2:]
            required_params = get_required_params(func=command_obj.process, remove_values=['self', 'request'])

            params_filled = []
            required_param_didnt_fill = []
            filled_all_required_param = True

            # Command.Meta.param_keywords (for keyword arguments), type: dict
            param_keywords = command_obj.Meta.param_keywords

            # Seperates the kwargs from args by -> loops through the param_keywords if the
            # keyword (eg: -u for username) is in 'args' then it adds the key
            # (convert the key from '-u' to 'username') and value to kwargs
            # then removed the key & value from args.
            for key, value in param_keywords.items():
                # eg: {'-u': 'username'}
                if value in args:
                    kwargs[key] = args[args.index(value) + 1]
                    args.remove(args[args.index(value) + 1])
                    args.remove(value)

            prefix = command_obj.Meta.kwarg_prefix  # truthy or falsy

            # if prefix truthy, it will allow extra keyword-args and adds it to kwargs.
            if prefix:
                # **kwargs must be in the class method if prefix (Command.Meta.kwarg_prefix) is truthy
                # show error if **kwargs not in the func / method
                if not accepts_kwargs(command_obj.process):
                    print("Error: You have enabled kwargs by setting kwarg_prefix, but your function doesn't have "
                          "**kwargs in the parameter.")
                    exit()

                # Converts & Adds extra keyword key, values to kwargs and then removes the key, value from args
                for arg in list(args):
                    # if the word (eg. -u) start with the prefix (eg. prefix = '-') then
                    # it will take it as a key, eg('-u')

                    if str(arg).startswith(prefix):
                        kwargs[arg[len(prefix):]] = args[args.index(arg) + 1]
                        args.remove(args[args.index(arg) + 1])
                        args.remove(arg)

            # After we move input-keyword-params from 'args' to 'kwargs' and clears the 'args' we
            # then add those args value and add it to params_filled list.
            # we add the func_params value by index, eg: our function(username, password), func_params are
            # ['username', 'password'] & in args we have ['username_value', 'password_value']
            # if we see using index 'username_value' is 'username' cuz both func_param value and args value have
            # the same index so we can ensure than the user has filled the username param and then we ca add
            # it to params_filled.

            for ind, arg in enumerate(args):
                try:
                    params_filled.append(func_params[ind])
                except IndexError:
                    pass

            # the same way we add kwargs key to params_filled
            for kwarg in kwargs.keys():
                params_filled.append(kwarg) if kwarg not in params_filled else ''

            # checking if the required params are filled, set filled_all_required_param = True if
            # all required params are filled.
            for arg in required_params:
                if arg not in params_filled:
                    required_param_didnt_fill.append(arg)
                    filled_all_required_param = False

            if not filled_all_required_param:
                raise RequiredArgumentNotProvidedError(command_obj=command_obj,
                                                       required_arg=required_param_didnt_fill[0])

            # the 'request' param in command object (Working on it)
            context = {}

            # Handle permissions if there are permissions for this command
            if command_dict['permissions']:
                for permission in command_dict['permissions']:
                    # Loops through all the given permissions, continue the process if permission granted
                    # otherwise, run on_permission_denied()
                    permission = permission()
                    has_permission = permission.process(request=context)

                    if not has_permission:
                        permission.on_permission_denied(request=context)
                        return

                    else:
                        pass

            try:
                return command_obj.process(context, *args, **kwargs)

            except TypeError as e:
                if not accepts_args(command_obj.process):
                    raise GotUnexpectedValueError(command_name=command_name, value=args[-1], command_obj=command_obj)

                elif accepts_args(command_obj.process):
                    raise GotMultipleValueError(command_name=command_name, command_obj=command_obj,
                                                arg_name=e.args[0].split(" ")[-1].replace("'", ''))
            except AttributeError as e:
                print("Error: ", e, ', To make the command class work add def process(self, request): attribute'
                                    'in your class.')
        else:
            raise CommandNotFoundError(command_name=command_name)

    def run(self):
        """
        Takes user input and runs the command and handles Errors.
        """

        try:
            prams = sys.argv[1:]  # removes the command name
            self.execute(prams)

        except RequiredArgumentNotProvidedError as e:
            e.command_obj.OnRequiredArgumentNotProvidedError(arg=e.required_arg, command_obj=e.command_obj)

        except CommandNotFoundError as e:
            if not self.on_command_not_found_error:
                print(f"Command {e.command_name} not found")
            else:
                self.on_command_not_found_error.on_error(command_name=e.command_name)

        except GotUnexpectedValueError as e:
            e.command_obj.OnGotUnexpectedvalueError(value=e.value, command_name=e.command_name)

        except GotMultipleValueError as e:
            e.command_obj.OnGotMultipleValueError(command_name=e.command_name, arg_name=e.arg_name)

    def set_on_command_not_found_error(self, obj: typing.Type[CliError]):
        self.on_command_not_found_error = obj()
