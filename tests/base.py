import os
import unittest
from cligo.cli import CliApp
from cligo.db.backends import SqliteDatabase

PARENT_DIR = os.path.dirname(__file__)


class CliGoTestCase(unittest.TestCase):

    def setUp(self):
        app = CliApp('Testapp')
        self.app = app

    def tearDown(self):
        pass


class CligoDBTestCase(unittest.TestCase):
    def setUp(self):
        database = SqliteDatabase(os.path.join(PARENT_DIR, 'temp_database.db'))
        CliApp.config(database)
        app = CliApp('Testapp')

        self.app = app

    def tearDown(self):
        CliApp.configuration.get('database').close()
        os.remove(os.path.join(PARENT_DIR, 'temp_database.db'))
