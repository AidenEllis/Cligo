class BasePermission:
    """
    A base class from which all permission classes should inherit.
    """

    request = {}

    def process(self):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def on_permission_denied(self):
        """
        Do something when permission in denied.
        """
        pass
