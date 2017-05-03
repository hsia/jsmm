#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright lixia@ccrise.com
'''

import os
import sys
import uuid
from datetime import datetime
from dateutil.relativedelta import *

os.chdir(os.path.dirname(__file__))
sys.path[:0] = ['app', 'lib']

from couchdb import CouchDB

couch_db = CouchDB('http://127.0.0.1:5984')
couchLucene_db = CouchDB('http://127.0.0.1:5986')


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


def get_retire_time(birthday, gender):
    start_date = datetime.strptime(birthday, "%Y-%m-%d")
    if gender == '男':
        return (start_date + relativedelta(years=+65)).strftime('%Y-%m-%d')
    else:
        return (start_date + relativedelta(years=+60)).strftime('%Y-%m-%d')


def formatter_time(input_date, formatter, formatter2='%Y.%m.%d'):
    if input_date and input_date != u'至今':
        return datetime.strptime(input_date, formatter).strftime(formatter2)
    else:
        return ''
