from datetime import datetime
import os, urllib

import feedparser
from bs4 import BeautifulSoup

import postgresql_database, mongo_database


SOURCE = 'http://feeds.reuters.com/reuters/topNews'

def _content(link):
    f = urllib.request.urlopen(link)
    soup = BeautifulSoup(f.read(), 'html.parser')
    f.close()
    content = soup.find('div', {'class': 'StandardArticleBody_body'})
    return "\n".join([_.string for _ in content.find_all('p') if _.string]) if content else ""

def _insert_entries (insert_function):
    entries = feedparser.parse(SOURCE)['entries']
    for entry in entries:
        insert_function(
            entry['link'],
            entry['title'],
            entry['summary'],
            _content(entry['link']),
            datetime.strptime(entry['published'], '%a, %d %b %Y %H:%M:%S %z')
        )
    return len(entries)

def run_postgresql():
    return _insert_entries(postgresql_database.insert)
    
def run_mongo():
    return _insert_entries(mongo_database.insert)
