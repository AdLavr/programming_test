import postgresql
import os

from postgresql_config import *

_database = None
try:
    _database = postgresql.open('pq://{}:{}@{}:{}/{}'.format(USER_LOGIN, USER_PASSWORD, URL, PORT, DATABASE_NAME))
except:
    pass

def run_server():
    global _database
    os.system(RUN_SERVER_COMMAND)
    _database = postgresql.open('pq://{}:{}@{}:{}/{}'.format(USER_LOGIN, USER_PASSWORD, URL, PORT, DATABASE_NAME))

def stop_server():
    global _database
    _database.close()
    os.system(STOP_SERVER_COMMAND)

def create_schema():
    _database.execute(
        "CREATE SCHEMA IF NOT EXISTS {0};"
        "CREATE TABLE IF NOT EXISTS {0}.{1} ("
        "id SERIAL PRIMARY KEY NOT NULL,"
        "link VARCHAR(256) NOT NULL,"
        "title VARCHAR(256) NOT NULL,"
        "summary VARCHAR(2048) NOT NULL,"
        "content VARCHAR(65536) NOT NULL,"
        "published TIMESTAMPTZ NOT NULL);".format(SCHEMA_NAME, TABLE_NAME)
    )

def insert(link, title, summary, content, published):
    insert_ = _database.prepare(
        "INSERT INTO {}.{} (link, title, summary, content, published) VALUES ($1, $2, $3, $4, $5)".format(
            SCHEMA_NAME,
            TABLE_NAME
        )
    )
    return insert_(link, title, summary, content, published)

def select_by_date(date):
    select = _database.prepare(
        "SELECT id, link, title, summary, content, published "
        "FROM {}.{} "
        "WHERE published::date = $1::date".format(SCHEMA_NAME, TABLE_NAME)
    )
    return select(date)

def clear():
    return _database.query("DELETE FROM {}.{}".format(SCHEMA_NAME, TABLE_NAME))
