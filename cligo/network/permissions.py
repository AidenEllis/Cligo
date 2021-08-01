from cligo.permissions import BasePermission
from .connection import checkConnectivity


class CheckIsValidConnection(BasePermission):

    def process(self):
        return checkConnectivity()

    def on_permission_denied(self):
        print("No Internet connection, Check your Internet connection and try again.")
