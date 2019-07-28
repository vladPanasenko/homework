from peewee import *

db = SqliteDatabase('top_by_keywords.db')

#
# class Top(Model):
#     query = TextField()
#     link = TextField()
#     position = IntegerField()
#     date = TextField()


class Top(Model):
    link = TextField()
    date = TextField()
    position = IntegerField()
    keyword = TextField()

    class Meta:
        database = db


if __name__ == "__main__":
    db.create_tables([Top])
