import sqlite3 as lite
import sys
from peewee import *
from datetime import date

# Do I have sqlite installed?
print 'driver version ' + lite.version
# need an 'expect' or something

con = None

try:
    con = lite.connect('test.db')

    cur = con.cursor()
    cur.execute('SELECT SQLITE_VERSION()')

    data = cur.fetchone()

    print "SQLite version: %s" % data

except lite.Error, e:

    print "Error %s:" % e.args[0]
    sys.exit(1)

finally:

    if con:
        con.close()


# try out the ORM
# http://stackoverflow.com/questions/9026069/python-lightweight-database-wrapper-for-sqlite
# http://docs.peewee-orm.com/en/latest/peewee/installation.html


db = SqliteDatabase('test.db')


class Person(Model):
    name = CharField()
    birthday = DateField()
    is_relative = BooleanField()

    class Meta:
        database = db  # This model uses the "people.db" database.


class Pet(Model):
    owner = ForeignKeyField(Person, related_name='pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db  # this model uses the "test.db" database


db.connect()

# create the tables
db.create_tables([Person, Pet])

# create my people
uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15), is_relative=True)
uncle_bob.save()

grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1), is_relative=True)
herb = Person.create(name='Herb', birthday=date(1950, 5, 5), is_relative=False)

grandma.name = 'Grandma L.'
grandma.save()
herb.save()

# create my animals

bob_kitty = Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')
herb_fido = Pet.create(owner=herb, name='Fido', animal_type='dog')
herb_mittens = Pet.create(owner=herb, name='Mittens', animal_type='cat')
herb_mittens_jr = Pet.create(owner=herb, name='Mittens Jr', animal_type='cat')

herb_mittens.delete_instance()  # he had a great life

herb_fido.owner = uncle_bob
herb_fido.save()
bob_fido = herb_fido  # rename our variable for clarity

# print out people

for person in Person.select().order_by(Person.birthday.desc()):
    print person.name, person.birthday

# print out pets that belong to people:

subquery = Pet.select(fn.COUNT(Pet.id)).where(Pet.owner == Person.id)
query = (Person
         .select(Person, Pet, subquery.alias('pet_count'))
         .join(Pet, JOIN.LEFT_OUTER)
         .order_by(Person.name))

for person in query.aggregate_rows():  # Note the `aggregate_rows()` call.
    print person.name, person.pet_count, 'pets'
    for pet in person.pets:
        print '    ', pet.name, pet.animal_type


# drop all tables
db.drop_tables([Person, Pet])
# close connection
db.close()



