from cligo.permissions.base import BasePermission
from tests.utils.exceptions import PermissionDenied, DummyFalse, Working


class TestPermissionTrue(BasePermission):

    def process(self):
        return True

    def on_permission_denied(self):
        raise PermissionDenied()


class TestPermissionFalse(BasePermission):

    def process(self):
        return False

    def on_permission_denied(self):
        raise PermissionDenied()


class TestPermissionFlaseDummyFalse(BasePermission):

    def process(self):
        return False

    def on_permission_denied(self):
        raise DummyFalse()


class TestPermissionRaisesWorking(BasePermission):

    def process(self):
        raise Working()

    def on_permission_denied(self):
        raise PermissionDenied()
