import inspect


def get_func_args(func, remove_vals=None) -> list[str]:
    """Get function arguments, varargs, kwargs and defaults.

    This function will be called whenever a exception is raised."""
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
    """Loops through the values list and removes it from the_list"""

    list_ = the_list
    for value in values:
        try:
            list_.remove(value)
        except ValueError:
            pass

    return list_


def accepts_kwargs(func):
    """returns True if the func have **kwargs else False"""
    return 'kwargs' in list(inspect.signature(func).parameters)


def accepts_args(func):
    """returns Bool if the func have *args else False"""
    return 'args' in list(inspect.signature(func).parameters)


def get_default_params(func):
    """Gets func's default params"""

    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }


def get_required_params(func, remove_values: list = None):
    """Gets func's required params"""

    if remove_values is None:
        remove_values = ['self']

    remove_values.extend(list(get_default_params(func).keys()))
    params = removeValueFromList(values=remove_values, the_list=list(inspect.getargs(func.__code__)[0]))

    return params


def getFuncParamInfo(func, param, fallback_type='', fallback_default_value='', convert_type_to_name=False):
    info = {}
    sig = inspect.signature(func).parameters.get(param)

    info['name'] = sig.name
    info['default_value'] = sig.default

    if convert_type_to_name:
        info['type'] = sig.annotation.__name__
    else:
        info['type'] = sig.annotation

    if sig.default == inspect.Signature.empty:
        info['default_value'] = fallback_default_value

    if sig.annotation == inspect.Signature.empty:
        info['type'] = fallback_type

    return info
