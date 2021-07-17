class BasePermission:
    """
    A base class from which all permission classes should inherit.
    """

    def process(self, request):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def on_permission_denied(self, request):
        """
        Do something when permission in denied.
        """
        pass
