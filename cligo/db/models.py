from peewee import Model as BaseModel
from cligo.cli import CliApp


__all__ = ['Model']


class Model(BaseModel):
    """
    A base class from which all model classes should inherit.
    """

    class Meta:
        database = CliApp.configuration.get('database')
