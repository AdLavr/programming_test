from datetime import timedelta
import os

from pymongo import MongoClient

from mongo_config import *


_client = None
_database = None
try:
    _client = MongoClient('mongodb://{}:{}'.format(URL, PORT))
    _database = _client[DATABASE_NAME]
except:
    pass

def run_server():
    os.system(RUN_SERVER_COMMAND)

def stop_server():
    _database = None
    _client = None
    os.system(STOP_SERVER_COMMAND)

def insert(link, title, summary, content, published):
    return _database[COLLECTION_NAME].insert_one({
        'link' : link,
        'title' : title,
        'summary' : summary,
        'content' : content,
        'published' : published
    })

def select_by_date(date):
    return list(_database[COLLECTION_NAME].find({
        'published': {
            '$gte': date,
            '$lt': date + timedelta(days=1)
        }
    }))

def clear():
    _database[COLLECTION_NAME].remove()
