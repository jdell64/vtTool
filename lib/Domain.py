import datetime
from peewee import *

db = SqliteDatabase('vtTool.db')


class Domain(Model):
    # todo: unique index on name
    name = CharField(unique=True)
    # todo: set date_added to default to now
    created_on = DateTimeField(default=datetime.datetime.now, null=False)
    last_modified = DateTimeField(default=datetime.datetime.now, null=False)
    last_scanned = DateTimeField(unique=False, null=True)
    # todo: status default 'new'
    status = CharField(default='new', null=False)
    # todo number_of_detections = 0
    number_of_detections = IntegerField(default=0, null=False)

    # New Fields
    vt_safety_score = IntegerField(null=True)
    vt_number_of_ips = IntegerField(null=True)


    class Meta:
        database = db

    # todo: read more on this
    # http://stackoverflow.com/questions/17134653/difference-between-class-and-instance-methods
    # https://julien.danjou.info/blog/2013/guide-python-static-class-abstract-methods
    # TODO: create a find or create method with kwargs
    @classmethod
    def find_or_create_by_name(cls, n):
        try:
            d = cls(name=n)
            d.save()
        except IntegrityError as e:
            if "UNIQUE constraint failed" in e.message or 'column name is not unique' in e.message:
                d = cls.get(cls.name == n)
            else:
                raise

        return d

    def to_string(self):
        # todo: finish this
        return "{Domain: {name: {%s}, created_on:{%s}, last_modified:{%s}, last_scanned:{%s}, status:{%s}, " \
               "number_of_detections:{%s} }}" % (self.name, self.created_on, self.last_modified,
                                                 self.last_scanned, self.status, self.number_of_detections)
