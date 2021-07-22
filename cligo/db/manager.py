class ModelRegister:
    """
    Regsiters models by crating database tables.
    """

    def __init__(self, database):
        self.database = database

    def register(self, models: list = None):
        if models:
            self.database.create_tables(models)


class DBManager:
    """
    Database Maager, for managing database, creating tables, registering Models
    """
    def __init__(self, database):
        self.models = ModelRegister(database)
