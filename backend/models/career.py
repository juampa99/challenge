from database import db
from pony.orm import Required, Set, PrimaryKey

class Career(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, max_len=100)
    inscription_year = Required(int)

    lead = Required('Lead')

    subjects = Set('Subject')

