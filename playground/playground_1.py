def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return layer


@parametrized
def regsiter(f, n):
    print(n)
    print(f)
    def aux(*xs, **kws):
        return f(*xs, **kws)

    return aux


@regsiter('trellect')
def login():
    print('logging in...')
    return True

login()