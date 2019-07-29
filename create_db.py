from peewee import *

db = SqliteDatabase('top_by_keywords.db')


class Top(Model):
    link = TextField()
    date = TextField()
    position = IntegerField()
    # keyword = ForeignKeyField(Keyword)

    class Meta:
        database = db


if __name__ == "__main__":
    db.create_tables([Top])
