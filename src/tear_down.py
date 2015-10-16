__author__ = 'jeff'

from peewee import *

from lib.Domain import Domain



# todo: ask if user is sure

db = SqliteDatabase('vtTool.db')

db.connect()
db.drop_tables([Domain])

db.close()
