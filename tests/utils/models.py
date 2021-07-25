from cligo.db import models


class User(models.Model):
    username = models.CharField()