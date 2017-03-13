#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import time
import urllib

import tornado.web
import tornado_utils
from tornado.httpclient import HTTPClient, HTTPError, HTTPRequest

from commons import couch_db, make_uuid, couchLucene_db
from lib.couchdb import CouchDB


@tornado_utils.bind_to(r'/documents/?')
class DocumentHandler(tornado.web.RequestHandler):
    def get(self):
        '''
        修改_id为member_id的member对象。
        '''
        response = couch_db.get(r'/jsmm/_design/documents/_view/by-memberid')
        doucmentList = json.loads(response.body.decode('utf-8'))
        documents = []
        for row in doucmentList['rows']:
            documents.append(row['value'])
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(documents))

    def post(self):
        '''
        修改_id为member_id的member对象。
        '''
        params = json.loads(self.request.body.decode('utf-8'))

        pageNumber = params['page']
        pageSize = params['rows']

        if ('branch' not in params):
            pass
        else:  # 如果有按机构查询的操作
            organName = params['branch']
            postParam = {"keys": [organName]}

        if ('order' not in params):
            order = True
        else:
            order = ((params['order'] == 'desc') and True or False)

        if ('branch' not in params or params['branch'] == '北京市' or params['branch'] == '朝阳区'):
            response = couch_db.get(
                '/jsmm/_design/documents/_view/by_memberid?limit=%(pageSize)s&skip=%(pageNumber)s&descending=%(order)s' % {
                    'pageSize': pageSize, 'pageNumber': (pageNumber - 1) * pageSize, 'order': order})
        else:  # 如果有按机构查询的操作
            # 查询未分页前数据总数(根据返回的Rows获得总数据量)#
            responseCount = couch_db.post('/jsmm/_design/documents/_view/by_branch', postParam)
            # 查询分页数据#
            response = couch_db.post(
                '/jsmm/_design/documents/_view/by_branch?limit=%(pageSize)s&skip=%(pageNumber)s&descending=%(order)s' % {
                    'pageSize': pageSize, 'pageNumber': (pageNumber - 1) * pageSize, 'order': order},
                postParam)

        documentList = json.loads(response.body.decode('utf-8'))
        documents = []
        documnetsResult = {}

        for row in documentList['rows']:
            documents.append(row['value'])

        documnetsResult['pageSize'] = pageSize
        documnetsResult['pageNumber'] = pageNumber

        if ('branch' not in params or params['branch'] == '北京市' or params['branch'] == '朝阳区'):
            documnetsResult['total'] = documentList['total_rows']
        else:  # 如果有按机构查询的操作
            documentListCount = json.loads(responseCount.body.decode('utf-8'))
            # 将分页前查询的总数返回给前台#
            documnetsResult['total'] = len(documentListCount['rows']);

        documnetsResult['rows'] = documents
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(documnetsResult))


@tornado_utils.bind_to(r'/documentSearch/?')
class DocumentHandlerSearch(tornado.web.RequestHandler):
    def post(self):
        '''
        修改_id为member_id的member对象。
        '''
        params = json.loads(self.request.body.decode('utf-8'))

        pageNumber = params['page']
        pageSize = params['rows']

        paramsStr = ""
        docType = params["documentInfo"]["docType"]
        name = params["documentInfo"]["name"]
        fileName = params["documentInfo"]["fileName"]
        startDate = params["documentInfo"]["startDate"]
        endDate = params["documentInfo"]["endDate"]
        branch = params["documentInfo"]["branch"]

        if docType != '':
            paramsStr += 'docType:"' + docType + '"'

        if name != '' and paramsStr != '':
            paramsStr += ' AND name:"' + name + '"'
        elif name != '' and paramsStr == '':
            paramsStr += 'name:"' + name + '"'

        if fileName != '' and paramsStr != '':
            paramsStr += ' AND fileName:"' + fileName + '"'
        elif fileName != '' and paramsStr == '':
            paramsStr += 'fileName:"' + fileName + '"'

        if startDate != '' and endDate != '' and paramsStr != '':
            paramsStr += ' AND fileUploadTime<date>:[' + startDate + ' TO ' + endDate + ']'
        elif startDate != '' and endDate != '' and paramsStr == '':
            paramsStr += 'fileUploadTime<date>:[' + startDate + ' TO ' + endDate + ']'

        if branch != '' and paramsStr != '' and branch == '北京市' and branch == '朝阳区':
            paramsStr += ' AND branch:"' + branch + '"'
        elif branch != '' and paramsStr == '' and branch == '北京市' and branch == '朝阳区':
            paramsStr += 'branch:"' + branch + '"'

        print('paramsStr = ' + paramsStr)
        if paramsStr != '':
            response = couchLucene_db.get(
                r'/_fti/local/jsmm/_design/documents/by_doc_info?q=%(paramsStr)s&limit=%(limit)s&skip=%(skip)s' % {
                    "paramsStr": urllib.parse.quote(paramsStr, "utf-8"), 'limit': pageSize,
                    'skip': (pageNumber - 1) * pageSize})
        else:
            response = couch_db.get(
                '/jsmm/_design/documents/_view/by_memberid?limit=%(pageSize)s&skip=%(pageNumber)s' % {
                    'pageSize': pageSize, 'pageNumber': (pageNumber - 1) * pageSize})
        documentList = json.loads(response.body.decode('utf-8'))

        documentsResult = {};
        documents = []

        if paramsStr != '':
            for row in documentList['rows']:
                row['fields']['_id'] = row['id']
                documents.append(row['fields'])
        else:
            for row in documentList['rows']:
                documents.append(row['value'])

        documentsResult['pageSize'] = pageSize
        documentsResult['pageNumber'] = pageNumber
        documentsResult['total'] = documentList['total_rows'];
        documentsResult['rows'] = documents

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(documentsResult))
