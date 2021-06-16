from peewee import *
from ..app import db_wrapper


class Driver(db_wrapper.Model):
    abbr = CharField(max_length=3, unique=True)
    name = CharField()
    car = CharField()
    start = DateTimeField()
    end = DateTimeField()
