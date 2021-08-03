import colorama
from cligo.output.outputHandler import outputData
from cligo.core.templates import getCommandHelpTemplate
from cligo.utils.funcTools import get_func_args, get_required_params, removeValueFromList, getFuncParamInfo


colorama.init()


class Command:
    """
    A base class from which all permission classes should inherit.
    """

    permissions = []
    request = {}

    def OnRequiredArgumentNotProvidedError(self, arg, command_obj):
        """Handles OnRequiredArgumentNotProvidedError"""
        print(f"Fill the required argument: <{arg}>")

    def OnGotUnexpectedvalueError(self, command_name, value):
        """Handles OnGotUnexpectedvalueError"""
        print(f"Command <{command_name}> got unexpected value '{value}'")

    def OnGotMultipleValueError(self, command_name, arg_name):
        """Handles OnGotMultipleValueError"""
        print(f"Command <{command_name}> got multiple values for argument '{arg_name}'")

    def help(self, command_name):
        params = get_func_args(self.process, remove_vals=['self', 'request'])
        required_params = get_required_params(self.process, remove_values=['request'])
        optional_params = removeValueFromList(required_params, list(params))

        params_info = {}

        for param in params:
            params_info[param] = getFuncParamInfo(self.process, param, convert_type_to_name=True)

            if param in required_params:
                params_info[param]['param_type'] = 'required'
            elif param in optional_params:
                params_info[param]['param_type'] = 'optional'

        param_keywords = self.Meta.param_keywords

        for param_info in params_info.values():
            param_keyword = param_keywords.get(param_info['name'], '')
            params_info[param_info['name']]['keyword'] = param_keyword

        print(getCommandHelpTemplate(argsinfo=params_info, command_name=command_name))

    @staticmethod
    def output(text, *args, string_format=False, **kwargs):
        """Color supported output"""
        data = outputData(template=text, string_format=string_format)
        print(data, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        pass

    @staticmethod
    def quit():
        exit()

    class Meta:
        param_keywords = {}
        kwarg_prefix = None
        help_keywords = []
        option_prefix = None
