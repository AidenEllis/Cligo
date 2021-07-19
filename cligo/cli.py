from cligo import process
from cligo.core.error import CliError
from cligo.exceptions import *
from .utils.funcTools import *
from cligo.command import Command


class CliApp:

    def __init__(self, name: str):
        self.name = name
        self.commands = process.commands
        self.on_command_not_found_error = None

    @staticmethod
    def register(command_obj, command_name):
        if not issubclass(command_obj, Command):
            raise NotACommandSubClassError(command_obj.__name__)
        process.commands[command_name] = {
            'command': command_obj,
            'permissions': command_obj.permissions
        }

    def execute(self, prams: list):
        command_name = prams[0]
        input_prams = prams[1:]

        args = list(input_prams)
        kwargs = {}

        if command_name in self.commands:
            command_dict = self.commands[command_name]
            command_obj_ = command_dict['command']  # not called
            command_obj = command_dict['command']()  # called

            func_args = get_func_args(func=command_obj.process, remove_vals=['*args', '**kwargs'])[2:]
            required_args = get_required_params(func=command_obj.process, remove_values=['self', 'request'])

            params_filled = []
            required_param_didnt_fill = []
            filled_all_required_param = True

            # based on kwarg params
            kwarg_params = command_obj.Meta.kwarg_keywords

            for k, v in kwarg_params.items():
                if v in args:
                    kwargs[k] = args[args.index(v) + 1]
                    args.remove(args[args.index(v) + 1])
                    args.remove(v)

            prefix = command_obj.Meta.kwarg_prefix  # if truthy, it will allow extra **kwargs and add it to kwargs

            if prefix:
                if not accepts_kwargs(command_obj_.process):
                    print("Error: You have enabled kwargs by setting kwarg_prefix, but your function doesn't have "
                          "**kwargs in the parameter.")
                    exit()

                for arg in list(args):
                    if str(arg).startswith(prefix):
                        kwargs[arg[len(prefix):]] = args[args.index(arg) + 1]
                        v = args[args.index(arg) + 1]
                        args.remove(arg)
                        args.remove(v)

            for ind, arg in enumerate(args):
                try:
                    params_filled.append(func_args[ind])
                except IndexError:
                    pass

            for kwarg in kwargs.keys():
                params_filled.append(kwarg) if kwarg not in params_filled else ''

            for arg in required_args:
                if arg not in params_filled:
                    required_param_didnt_fill.append(arg)
                    filled_all_required_param = False

            if not filled_all_required_param:
                raise RequiredArgumentNotProvidedError(command_obj=command_obj,
                                                       required_arg=required_param_didnt_fill[0])

            context = {}
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

    def run(self, prams):
        try:
            prams = prams[1:]
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

    def set_on_command_not_found_error(self, obj: CliError):
        self.on_command_not_found_error = obj
