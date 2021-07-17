from process import commands


def parametrized(dec):
    """
    A decorator to prametrize another decorator, in this way you can
    add prams to your decorators.

    @parametrized
    def my_decorator(name):
        def wrapper(*args, **kwargs):
            do_something()
            return func(*args, **kwargs)

        return wrapper

    @my_decorator(name='name_pram')
    def foo():
        print('this is a foo func.')

    """
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return layer


@parametrized
def register(func, command_name: str):
    print(func)
    commands[command_name] = func

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
