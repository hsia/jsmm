#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import random

from tornado.httpclient import HTTPError

from commons import couch_db, make_uuid


def try_(operation_result):
    if isinstance(operation_result, Exception):
        raise operation_result


# ！！！注意：此处会删除原有的数据库！！！
if not isinstance(couch_db.get('/jsmm'), HTTPError):
    try_(couch_db.delete('/jsmm'))
try_(couch_db.put('/jsmm'))

# members = ['Ulysses Francis', 'Rolf Tel', 'Kaiden Michi', 'Dallas Billie', 'Warren Granville',
#            '林丹娜', 'Hyram Makoto', '杨爱丽', 'Cary Cheyenne', 'Temple Colbert', 'Delroy Naoki',
#            'Bishop Arthur', 'Yori Shiro', 'zhangsan', 'lisi', 'wangwu', 'zhaoliu', 'tianqi']
# for member in members:
#     try_(couch_db.post('/jsmm', {
#         'type': 'member',
#         '_id': make_uuid(),
#         'name': member,
#         'age': math.ceil(random.uniform(16, 90))
#     }))

try_(couch_db.put('/jsmm/_design/members', {
    'views': {
        'all': {
            'map':
                '''function(doc) {
                  if (doc.type == 'member') {
                    emit([doc.id, doc.name], doc);
                  }
                }'''
        },
        'by-name': {
            'map':
                '''function (doc) {
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

try_(couch_db.put('/jsmm/_design/documents', {
    'views': {
        'all': {
            'map':
                '''function (doc) {
        if (doc.departmentReport != null || doc.departmentInfo != null || doc.speechesText != null) {
            var result = {};
            for (var i in doc.departmentReport) {
                result.name = doc.name;
                result.branch = doc.branch;
                result.type = 'report';
                result.fileName = doc.departmentReport[i].depReportName;
                result.uploadTime = doc.departmentReport[i].depReportTime;
                result.file_url = doc.departmentReport[i].file_url;
                emit([result.branch,result.name,result.type,result.uploadTime,result.fileName], result);
                result = {};
            }
            for (var j in doc.departmentInfo) {
                result.name = doc.name;
                result.branch = doc.branch;
                result.type = 'info';
                result.fileName = doc.departmentInfo[j].depReportName;
                result.uploadTime = doc.departmentInfo[j].depReportTime;
                result.file_url = doc.departmentInfo[j].file_url;
                emit([result.branch,result.name,result.type,result.uploadTime,result.fileName], result);
                result = {};
            }
            for (var k in doc.speechesText) {
                result.name = doc.name;
                result.branch = doc.branch;
                result.type = 'speech';
                result.fileName = doc.speechesText[k].speechesTextName;
                result.uploadTime = doc.speechesText[k].speechesTextTime;
                result.file_url = doc.speechesText[k].file_url;
                emit([result.branch,result.name,result.type,result.uploadTime,result.fileName], result);
                result = {};
            }
        }

    }'''
        }
    }
}))

try_(couch_db.put('/jsmm/_design/documents', {
    'views': {
        'by-branch': {
            'map':
                '''function (doc) {
        if (doc.departmentReport != null || doc.departmentInfo != null || doc.speechesText != null) {
            var result = {};
            for (var i in doc.departmentReport) {
                result.name = doc.name;
                result.branch = doc.branch;
                result.type = 'report';
                result.fileName = doc.departmentReport[i].depReportName;
                result.uploadTime = doc.departmentReport[i].depReportTime;
                result.file_url = doc.departmentReport[i].file_url;
                emit(result.branch, result);
                result = {};
            }
            for (var j in doc.departmentInfo) {
                result.name = doc.name;
                result.branch = doc.branch;
                result.type = 'info';
                result.fileName = doc.departmentInfo[j].depReportName;
                result.uploadTime = doc.departmentInfo[j].depReportTime;
                result.file_url = doc.departmentInfo[j].file_url;
                emit(result.branch, result);
                result = {};
            }
            for (var k in doc.speechesText) {
                result.name = doc.name;
                result.branch = doc.branch;
                result.type = 'speech';
                result.fileName = doc.speechesText[k].speechesTextName;
                result.uploadTime = doc.speechesText[k].speechesTextTime;
                result.file_url = doc.speechesText[k].file_url;
                emit(result.branch, result);
                result = {};
            }
        }
                }'''
        }
    }
}))
