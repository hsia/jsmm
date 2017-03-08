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

try_(couch_db.put('/jsmm/_design/members', {
    'views': {
        'all': {
            'map': '''
function(doc) {
  if (doc.type == 'member') {
    emit([doc.id, doc.name], doc);
  }
}'''
        },
        'by-name': {
            'map': '''
function (doc) {
  if (doc.type == 'member') {
    if(doc.name) {
    var name = doc.name.replace(/^(A|The) /, '');
    emit(name, doc);
    }
  }
}'''
        },
        'by-memberid': {
            'map': '''
function (doc) {
  if(doc.type == 'document'){
    emit(doc.memberId, doc);
  }
}'''
        }
    },
    'fulltext': {
        'by_basic_info': {
            'analyzer': 'chinese',
            'index': '''
function (doc) {
  var result = new Document();
  function makeIndex(obj, field, store, type) {
    var value = null;
    field = field || 'default';
    store = store || 'no';
    type = type || 'text';
    if (field != 'default') {
      value = obj[field];
    }
    switch (type) {
      case 'date':
        if (!value) break;
        value = value.split('-');
        result.add(new Date(value[0], value[1], value[2]), {'field': field, 'store': store, 'type': 'date'});
        break;
      default:
        result.add(value, {'field': field, 'store': store, 'type': type});
        break;
    }
  }
  if (doc.type == 'member') {
    makeIndex(doc, 'name', 'yes');
    makeIndex(doc, 'gender', 'yes');
    makeIndex(doc, 'idCard', 'yes');
    makeIndex(doc, 'nation', 'yes');
    makeIndex(doc, 'birthPlace', 'yes');
    makeIndex(doc, 'birthday', 'yes', 'date');
    makeIndex(doc, 'branch', 'yes');
    makeIndex(doc, 'branchTime', 'yes', 'date');
    doc.agencybroker.forEach(function(introducer) {
      makeIndex(introducer, 'agencyName', 'yes');
    });
    return result;
  } else {
    return null;
  }
}'''
        }
    }
}))

try_(couch_db.put('/jsmm/_design/documents', {
    'views': {
        'all': {
            'map':
                '''
                function (doc) {
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
                }

                '''
        },
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
    }
'''
        }
    }
}))
