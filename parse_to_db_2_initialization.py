from peewee import *

db = SqliteDatabase('hw_part_1.db')


class AdvNum(Model):
    adv_url = TextField()

    class Meta:
        database = db


class AdvTitlePrice(Model):
    title = TextField()
    price = TextField()

    class Meta:
        database = db


if __name__ == "__main__":
    db.create_tables([AdvNum, AdvTitlePrice])

