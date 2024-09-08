from database import db
from pony.orm import Required, Database, PrimaryKey


class Subject(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, max_len=100)
    times_taken = Required(int)
    weekly_hours = Required(int)

    career = Required("Career")

