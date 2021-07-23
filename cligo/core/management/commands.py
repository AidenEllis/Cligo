from cligo import __version__


def commandManager(args):
    """
    Built in cligo command manager.
    We call this in Terminal :
    C:/Some/Path> cligo <some_command>
    """
    if not args:
        exit()

    if args[0] == "test":
        print(f"Test is Working. Arg: {args[0]}")

    elif args[0] == " --version":
        print(f"Cligo v{__version__}")

