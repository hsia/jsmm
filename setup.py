#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
    "views": {
        "by_branch": {
            "map": "\nfunction (doc) {\n  if(doc.type == 'document'){\n    emit(doc.branch, doc);\n  }\n}"
        },
        "by_memberid": {
            "map": "\nfunction (doc) {\n  if(doc.type == 'document'){\n    emit(doc.memberId, doc);\n  }\n}"
        }
    },
    "fulltext": {
        "by_attachment": {
            "index": "\n                function(doc) {\n                  var result = new Document();\n                  if (doc.type == 'document') {\n                    for(var a in doc._attachments) {\n                      result.attachment(\"default\", a);\n                    }\n                    return result;\n                  } else {\n                    return null;\n                  }\n                }\n"
        },
        "by_doc_info": {
            "analyzer": "chinese",
            "index": "\nfunction (doc) {\n        var result = new Document();\n        function makeIndex(obj, field, store, type) {\n            var value = null;\n            field = field || 'default';\n            store = store || 'no';\n            type = type || 'text';\n            if (field != 'default') {\n                value = obj[field];\n            }\n                    result.add(value, {'field': field, 'store': store, 'type': type});}\n        if (doc.type == 'document') {\n            makeIndex(doc, 'fileName', 'yes');\n            makeIndex(doc, 'name', 'yes');\n            makeIndex(doc, 'branch', 'yes');\n            makeIndex(doc, 'fileUploadTime', 'yes', 'date');\n            makeIndex(doc, 'fileUploadTime', 'yes');\n            makeIndex(doc, 'docType', 'yes');\n            return result;\n        } else {\n            return null;\n        }\n    }"
        }
    }
}))
