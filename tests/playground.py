funcs_registry = []  # List of all functions decorated with @run_this_method


def run_this_method(m):
    global functions_registry
    funcs_registry.append(m)  # Add function/method to the registry

    def w(my_arg):
        _do_some_magic(my_arg, m)

    return w


def _do_some_magic(callback_arg, callback):
    if True:
        callback(callback_arg)


@run_this_method
def method_with_custom_name(my_arg):
    return "The args is: " + my_arg


def _init_and_run():
    global functions_registry

    # Here you can iterate over "functions_registry"
    # and do something with each function/method in it
    for m in functions_registry:
        print(m.__name__)


class FunDecorator:
    def __init__(self):
        self.registry = []

    def __call__(self, m):
        "This method is called when some method is decorated"
        self.registry.append(m)  # Add function/method to the registry

        def w(my_arg):
            _do_some_magic(my_arg, m)

        return w


run_this_method = FunDecorator()  # Create class instance to be used as decorator


@run_this_method
def method_with_custom_name(my_arg):
    return "The args is: " + my_arg


@run_this_method
def bruh():
    pass


# do some magic with each decorated method:
for m in run_this_method.registry:
    print(m.__name__)

