import os
import unittest
from cligo.cli import CliApp
from cligo.db.backends import SqliteDatabase


PARENT_DIR = os.path.dirname(__file__)
DB_NAME = 'temp_database.db'


class CliGoTestCase(unittest.TestCase):

    def setUp(self):
        app = CliApp('Testapp')
        self.app = app

    def tearDown(self):
        pass


class CligoDBTestCase(unittest.TestCase):
    def setUp(self):
        database = SqliteDatabase(os.path.join(PARENT_DIR, DB_NAME))
        CliApp.config(database)
        app = CliApp('Testapp')

        self.app = app

    def tearDown(self):
        CliApp.configuration.get('database').close()
        os.remove(os.path.join(PARENT_DIR, DB_NAME))
