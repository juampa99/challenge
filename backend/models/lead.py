from database import db
from pony.orm import Required, Set, PrimaryKey

class Lead(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, max_len=100)

    # These fields should be validated
    email = Required(str, max_len=320)
    address = Required(str, max_len=100)
    country = Required(str, max_len=100)
    phone = Required(str)

    careers = Set('Career')

