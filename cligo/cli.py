import sys
import typing
from cligo.exceptions import *
from .utils.funcTools import *
from .db.manager import DBManager
from cligo.command import Command
from .output.colors import colorText
from cligo.core.error import CliError
from .utils.dataTools import ObjectMapDict


__all__ = ['CliApp']


class CliApp:
    configuration = {}
    commands = {}
    database = DBManager(configuration.get('database'))

    def __init__(self, name: str):
        self.name = name
        self.commands = CliApp.commands
        self.on_command_not_found_error = None
        self.db = DBManager(CliApp.configuration.get('database'))

    @staticmethod
    def config(database=None):
        CliApp.configuration['database'] = database
        CliApp.configuration.get('database').connect()
        CliApp.database = DBManager(CliApp.configuration.get('database'))

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

        CliApp.commands[command_name] = {
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

            # request object (access it with self.request)
            request = ObjectMapDict()

            command_obj.request = request

            help_keywords = command_obj.Meta.help_keywords

            if args and args[0] in help_keywords and args[0] != "":
                command_obj.help(command_name)
                exit()

            # Command.Meta prefixes (truthy or falsy)
            option_prefix = command_obj.Meta.option_prefix
            kwarg_prefix = command_obj.Meta.kwarg_prefix

            if option_prefix and kwarg_prefix:
                if option_prefix == kwarg_prefix:
                    print(f"{colorText('Cligo Error: ', 'red')}: command's ({command_name}) "
                          f"{colorText('option_prefix', 'blue')} and {colorText('kwarg_prefix', 'blue')} can not be "
                          "same.")
                    exit()

            options_dict = ObjectMapDict()

            # Handling options and removing them from 'input_prams' & 'args'
            if option_prefix:
                for param in list(input_prams):
                    if str(param).startswith(option_prefix):
                        options_dict[param[2:]] = True
                        input_prams.remove(param)
                        args.remove(param)

            request['options'] = options_dict

            # parameters of the func / method
            func_params = get_func_args(func=command_obj.process, remove_vals=['*args', '**kwargs'])
            func_params.remove('self')

            required_params = get_required_params(func=command_obj.process, remove_values=['self'])

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

            # if prefix truthy, it will allow extra keyword-args and adds it to kwargs.
            if kwarg_prefix:
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

                    if str(arg).startswith(kwarg_prefix):
                        kwargs[arg[len(kwarg_prefix):]] = args[args.index(arg) + 1]
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

            if not filled_all_required_param and not input_prams:
                raise RequiredArgumentNotProvidedError(command_obj=command_obj,
                                                       required_arg=required_param_didnt_fill[0])

            if not filled_all_required_param and args and not input_prams[0] in param_keywords.values():
                raise RequiredArgumentNotProvidedError(command_obj=command_obj,
                                                       required_arg=required_param_didnt_fill[0])

            if not filled_all_required_param and not input_prams[0] in param_keywords.values():
                raise RequiredArgumentNotProvidedError(command_obj=command_obj,
                                                       required_arg=required_param_didnt_fill[0])

            # Handle permissions if there are permissions for this command
            if command_dict['permissions']:
                for permission in command_dict['permissions']:
                    # Loops through all the given permissions, continue the process if permission granted
                    # otherwise, run on_permission_denied()
                    permission = permission()
                    permission.request = request
                    has_permission = permission.process()

                    if not has_permission:
                        permission.on_permission_denied()
                        return

                    else:
                        pass

            try:
                return command_obj.process(*args, **kwargs)

            except TypeError as e:
                if not accepts_args(command_obj.process):
                    if (len(args) + len(kwargs)) > len(func_params):
                        raise GotUnexpectedValueError(command_name=command_name, value=args[-1],
                                                      command_obj=command_obj)

                raise GotMultipleValueError(command_name=command_name, command_obj=command_obj,
                                            arg_name=e.args[0].split(" ")[-1].replace("'", ''))
        else:
            raise CommandNotFoundError(command_name=command_name)

    def run(self, params=None):
        """
        Takes user input and runs the command and handles Errors.
        """

        try:
            if params:
                prams = params
            else:
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

    def run_from_terminal(self, command: str):
        """This is for test cases, alternative of run()"""
        params = str(command).split(" ")
        params.remove('python')
        params.remove('main.py')
        self.run(params=params)

    def set_on_command_not_found_error(self, obj: typing.Type[CliError]):
        self.on_command_not_found_error = obj()
