import os
os.chdir(os.path.dirname(__file__))

import sys
sys.path[:0] = ['app', 'lib']

from couchdb import CouchDB
couch_db = CouchDB('http://127.0.0.1:5984')

import uuid
def make_uuid():
    return uuid.uuid4().hex
