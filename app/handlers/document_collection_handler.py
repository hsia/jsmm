#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import urllib

import tornado.web
import tornado_utils

from commons import couch_db, couchLucene_db


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

        paramsStr = ""
        if "documentInfo" in params:
            # name = params["documentInfo"]["name"]
            # fileName = params["documentInfo"]["fileName"]
            keyWorld = params["documentInfo"]["keyWord"].replace(' ', '')
            keyWordAttachment = params["documentInfo"]["keyWordAttachment"]
            startDate = params["documentInfo"]["startDate"]
            endDate = params["documentInfo"]["endDate"]
            docType = params["documentInfo"]["docType"]

            if keyWordAttachment != '':
                paramsStr += keyWordAttachment
            else:
                pass

            # if name != '' and paramsStr != '':
            #     paramsStr += ' AND name:"' + name + '"'
            # elif name != '' and paramsStr == '':
            #     paramsStr += 'name:"' + name + '"'
            # else:
            #     pass
            #
            # if fileName != '' and paramsStr != '':
            #     paramsStr += ' AND fileName:"' + fileName + '"'
            # elif fileName != '' and paramsStr == '':
            #     paramsStr += 'fileName:"' + fileName + '"'
            # else:
            #     pass
            if keyWorld != '' and paramsStr != '':
                paramsStr += ' AND (fileName:' + keyWorld + ' OR name:' + keyWorld + ')'
            elif keyWorld != '' and paramsStr == '':
                paramsStr += '(fileName:' + keyWorld + ' OR name:' + keyWorld + ')'
            else:
                pass


            if startDate != '' and endDate != '' and paramsStr != '':
                paramsStr += ' AND fileUploadTime<date>:[' + startDate + ' TO ' + endDate + ']'
            elif startDate != '' and endDate != '' and paramsStr == '':
                paramsStr += 'fileUploadTime<date>:[' + startDate + ' TO ' + endDate + ']'
            else:
                pass

            if docType != '' and paramsStr != '':
                paramsStr += ' AND docType:"' + docType + '"'
            elif docType != '' and paramsStr == '':
                paramsStr += 'docType:"' + docType + '"'
            else:
                pass

        if "branch" in params:
            branch = params["branch"]

            if branch != '' and paramsStr != '' and branch != '北京市' and branch != '朝阳区':
                paramsStr += ' AND branch:"' + branch + '"'
            elif branch != '' and paramsStr == '' and branch != '北京市' and branch != '朝阳区':
                paramsStr += 'branch:"' + branch + '"'
            else:
                pass

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

        documentsResult = {}
        if response.code == 200:
            documents = []
            documentList = json.loads(response.body.decode('utf-8'))
            print(documentList)

            if paramsStr != '':
                for row in documentList['rows']:
                    row['fields']['_id'] = row['id']
                    documents.append(row['fields'])
            else:
                for row in documentList['rows']:
                    documents.append(row['value'])

            documentsResult['total'] = documentList['total_rows']
            documentsResult['rows'] = documents
        else:
            documentsResult['total'] = 0
            documentsResult['rows'] = []

        documentsResult['pageSize'] = pageSize
        documentsResult['pageNumber'] = pageNumber

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(documentsResult))
