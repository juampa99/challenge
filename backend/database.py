# database.py
from pony.orm import Database

db = Database()

def bind_db():
    db.bind(provider='sqlite', filename='database.db', create_db=True)
    db.generate_mapping(create_tables=True)

