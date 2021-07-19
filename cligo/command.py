class Command:
    """
    A base class from which all permission classes should inherit.
    """

    permissions = []

    def process(self, request, *args, **kwargs):
        """
        process the incoming request, doesn't need to return anything.
        It's all print based.
        """
        pass

    def OnRequiredArgumentNotProvidedError(self, arg, command_obj):
        """Handles OnRequiredArgumentNotProvidedError"""
        print(f"Fill the required argument: <{arg}>")

    def OnGotUnexpectedvalueError(self, command_name, value):
        """Handles OnGotUnexpectedvalueError"""
        print(f"Command <{command_name}> got unexpected value '{value}'")

    def OnGotMultipleValueError(self, command_name, arg_name):
        """Handles OnGotMultipleValueError"""
        print(f"Command <{command_name}> got multiple values for argument '{arg_name}'")

    def __call__(self, *args, **kwargs):
        pass

    @staticmethod
    def quit():
        exit()

    class Meta:
        param_keywords = None
        kwarg_prefix = None
