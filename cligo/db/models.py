from cligo.cli import CliApp
from peewee import Model as BaseModel
from peewee import (CharField, TextField, DateTimeField, IntegerField, BooleanField, FloatField,
                    DoubleField, BigIntegerField, DecimalField, PrimaryKeyField, ForeignKeyField,
                    DateField, TimeField, TimestampField, AutoField, FixedCharField,
                    UUIDField, IPField, BareField, BlobField, IdentityField,
                    SmallIntegerField, BigAutoField, BinaryUUIDField, BitField, BigBitField,
                    ManyToManyField, Field)


__all__ = ['CharField', 'TextField', 'DateTimeField', 'IntegerField', 'BooleanField', 'FloatField', 'DoubleField',
           'BigIntegerField', 'DecimalField', 'PrimaryKeyField', 'ForeignKeyField', 'DateField', 'TimeField',
           'TimestampField', 'AutoField', 'FixedCharField', 'UUIDField', 'IPField', 'BareField', 'BlobField',
           'IdentityField', 'SmallIntegerField', 'BigAutoField', 'BinaryUUIDField', 'BitField', 'BigBitField',
           'ManyToManyField', 'Field', 'Model']


class Model(BaseModel):
    class Meta:
        database = CliApp.configuration.get('database')
