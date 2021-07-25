class PermissionDenied(Exception):
    __module__ = Exception.__module__

    def __init__(self):
        message = f"Permission denied."
        self.message = message
        super().__init__(self.message)


class Working(Exception):
    __module__ = Exception.__module__

    def __init__(self):
        message = ""
        self.message = message
        super().__init__(self.message)


class DummyFalse(Exception):
    __module__ = Exception.__module__

    def __init__(self):
        message = ""
        self.message = message
        super().__init__(self.message)
