#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright lixia@ccrise.com
'''

import os
import sys
import uuid
from datetime import datetime

from couchdb import CouchDB

os.chdir(os.path.dirname(__file__))
sys.path[:0] = ['app', 'lib']

couch_db = CouchDB('http://127.0.0.1:5984')


def make_uuid():
    '''
    生成随机的UUID，并返回16进制字符串
    '''
    return uuid.uuid4().hex


def get_now():
    '''
    返回当前日期时间的ISO 8601格式字符串，格式为：YYYY-MM-DDTHH:MM:SS.mmmmmm
    '''
    return datetime.now().isoformat()
