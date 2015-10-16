__author__ = 'jeff'
from peewee import *
from lib.Domain import Domain

# db = SqliteDatabase('vtTool.db')

def setup(db):
    db.connect()
    db.create_tables([Domain])
    db.close()
def tear_down(db):
    # todo: ask if user is sure
    db = SqliteDatabase('vtTool.db')

    db.connect()
    db.drop_tables([Domain])

    db.close()
