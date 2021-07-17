def commandManager(args):
    """
    Built in cligo command manager.
    We call this in Terminal :
    C:/Some/Path> cligo <some_command>
    """
    if args[0] == "test":
        try:
            print(f"Test is Working. Arg: {args[1]}")
        except IndexError:
            print('Missing 1 Argument.')
