def commandManager(args):
    """
    Built in cligo command manager.
    We call this in Terminal :
    C:/Some/Path> cligo <some_command>
    """
    try:
        if args[0] == "test":
            print(f"Test is Working. Arg: {args[0]}")
    except IndexError:
        print('Please provide an argument.')
