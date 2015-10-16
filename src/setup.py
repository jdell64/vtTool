__author__ = 'jeff'
from peewee import *
from lib.Domain import Domain

db = SqliteDatabase('vtTool.db')


db.connect()
db.create_tables([Domain])

db.close()
