from peewee import *


db = SqliteDatabase('ads.db')


class Ad(Model):
    name = CharField(max_length=255, index=True)
    link = CharField(max_length=255)
    price = FloatField()
    city = CharField(max_length=255)
    time = CharField(max_length=255)

    class Meta:
        database = db


if __name__ == '__main__':
    db.create_tables([Ad])