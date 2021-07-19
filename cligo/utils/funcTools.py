import inspect


def get_func_args(func, remove_vals=None) -> list[str]:
    """
    Get function arguments, varargs, kwargs and defaults.
    """

    args, varargs, kwargs, defs = inspect.getfullargspec(func)[:4]

    if defs is not None:
        # If there are defaults, include them in the main argument list
        for i in range(-len(defs), 0):
            args[i] += ' = {}'.format(defs[i])

    if varargs is not None:
        # If the function accept extra arguments, include them at the end of the list.
        args.append('*' + varargs)

    if kwargs is not None:
        # If the function accept extra keyworded arguments, include them at the end of the list.
        args.append('**' + kwargs)

    for ind, val in enumerate(args):
        if "=" in str(val):
            args[ind] = str(val).split(" ")[0]

    if remove_vals:
        return removeValueFromList(values=remove_vals, the_list=args)

    return args  # args contain information about all the function arguments.


def removeValueFromList(values: list, the_list: list):
    list_ = the_list
    for value in values:
        try:
            list_.remove(value)
        except ValueError:
            pass

    return list_


def accepts_kwargs(func):
    return 'kwargs' in list(inspect.signature(func).parameters)


def accepts_args(func):
    return 'args' in list(inspect.signature(func).parameters)


def get_default_params(func):
    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }


def get_required_params(func, remove_values: list = None):
    if remove_values is None:
        remove_values = ['self']

    remove_values.extend(list(get_default_params(func).keys()))

    params = removeValueFromList(values=remove_values, the_list=list(inspect.getargs(func.__code__)[0]))

    return params
