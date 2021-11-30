import unittest
from cligo.cli import CliApp


class CliGoTestCase(unittest.TestCase):

    def setUp(self):
        app = CliApp('Testapp')
        self.app = app

    def tearDown(self):
        pass
