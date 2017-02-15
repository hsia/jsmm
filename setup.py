#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from commons import couch_db, make_uuid
import math
import random

def try_(operation_result):
    if isinstance(operation_result, Exception):
        raise operation_result

try_(couch_db.delete('/jsmm'))
try_(couch_db.put('/jsmm'))

members = ['Ulysses Francis', 'Rolf Tel', 'Kaiden Michi', 'Dallas Billie', 'Warren Granville', '林丹娜', 'Hyram Makoto', '杨爱丽', 'Cary Cheyenne', 'Temple Colbert', 'Delroy Naoki', 'Bishop Arthur', 'Yori Shiro']
for member in members:
    try_(couch_db.post('/jsmm', {
        'type': 'member',
        '_id': make_uuid(),
        'name': member,
        'age': math.ceil(random.uniform(16, 90))
    }))

try_(couch_db.put('/jsmm/_design/members', {
  'views' : {
    'all': {
      'map' : '''function(doc) {
        if (doc.type == 'member') {
          emit([doc.id, doc.name], doc);
        }
      }'''
    },
    'by-name' : {
      'map' : '''function (doc) {
        if (doc.type == 'member') {
          if(doc.name) {
              var name = doc.name.replace(/^(A|The) /, '');
              emit(name, doc);
          }
        }
      }'''
    }
  }
}))


