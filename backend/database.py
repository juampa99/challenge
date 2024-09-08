import psycopg2

from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from os import environ
from pony.orm import Database

def create_db_if_not_exists(dbname, user, password, host='localhost', port='5432'):
    con = psycopg2.connect(dbname='postgres', user=user, password=password, host=host, port=port)
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (dbname,))
    if not cur.fetchone():
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
        print(f"Database '{dbname}' created.")
    else:
        print(f"Database '{dbname}' already exists.")
    cur.close()
    con.close()


db = Database()

def bind_db(test=False):
    if test:
        filename = ":memory:"
        db.bind(provider="sqlite", filename=filename, create_db=True)
    else:

        create_db_if_not_exists("lead_api", user="postgres", password=environ["POSTGRES_PASSWORD"], host=environ["PG_HOST"])

        db.bind(provider='postgres', user="postgres", password=environ["POSTGRES_PASSWORD"], host=environ["PG_HOST"], database='lead_api')
    db.generate_mapping(create_tables=True)

