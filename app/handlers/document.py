#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import time, datetime
import tornado.web

import tornado_utils
from commons import couch_db, get_now, make_uuid


@tornado_utils.bind_to(r'/documents/?')
class DocumentHandler(tornado.web.RequestHandler):
    def get(self):
        '''
        修改_id为member_id的member对象。
        '''
        response = couch_db.get(r'/jsmm/_design/documents/_view/all')
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

        if ('organName' not in params):
            pass
        else:  # 如果有按机构查询的操作
            organName = params['organName']
            postParam = {"keys": [organName]}

        if ('order' not in params):
            order = True
        else:
            order = ((params['order'] == 'desc') and True or False)

        if ('organName' not in params or params['organName'] == '北京市' or params['organName'] == '朝阳区'):
            response = couch_db.get(
                '/jsmm/_design/documents/_view/all?limit=%(pageSize)s&skip=%(pageNumber)s&descending=%(order)s' % {
                    'pageSize': pageSize, 'pageNumber': (pageNumber - 1) * pageSize, 'order': order})
        else:  # 如果有按机构查询的操作
            # 查询未分页前数据总数(根据返回的Rows获得总数据量)#
            responseCount = couch_db.post('/jsmm/_design/documents/_view/by-branch', postParam)
            # 查询分页数据#
            response = couch_db.post(
                '/jsmm/_design/documents/_view/by-branch?limit=%(pageSize)s&skip=%(pageNumber)s&descending=%(order)s' % {
                    'pageSize': pageSize, 'pageNumber': (pageNumber - 1) * pageSize, 'order': order},
                postParam)

        documentList = json.loads(response.body.decode('utf-8'))
        documents = []
        documnetsResult = {}

        for row in documentList['rows']:
            documents.append(row['value'])

        documnetsResult['pageSize'] = pageSize
        documnetsResult['pageNumber'] = pageNumber

        if ('organName' not in params or params['organName'] == '北京市' or params['organName'] == '朝阳区'):
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
        searchInfo = params['searchInfo']

        # if ('order' not in params):
        #     order = True
        # else:
        #     order = ((params['order'] == 'desc') and True or False)

        response = couch_db.get('/jsmm/_design/documents/_view/all')
        documentList = json.loads(response.body.decode('utf-8'))
        documents = []
        documnetsResult = {}
        for row in documentList['rows']:
            # 对所有数据进行条件查询匹配，匹配成功则返回前台#
            rowValue = row['value'];
            if (searchInfo['branch'] == '' or searchInfo['branch'] == '北京市' or searchInfo['branch'] == '朝阳区'):
                branchResult = True;
            elif (rowValue['branch'].find(searchInfo['branch']) != -1):
                branchResult = True
            else:
                branchResult = False

            if ("type" not in searchInfo or searchInfo['type'] == ''):
                typeResult = True;
            elif (rowValue['type'].find(searchInfo['type']) != -1):
                typeResult = True
            else:
                typeResult = False

            if (searchInfo['name'] == ''):
                nameResult = True
            elif (rowValue['name'].find(searchInfo['name']) != -1):
                nameResult = True
            else:
                nameResult = False

            if (searchInfo['fileName'] == ''):
                fileNameResult = True;
            elif (rowValue['fileName'].find(searchInfo['fileName']) != -1):
                fileNameResult = True
            else:
                nameResult = False

            rowValueTime = time.mktime(time.strptime(rowValue['uploadTime'], '%Y-%m-%d %H:%M:%S'))
            if (searchInfo['startTime'] == '' and searchInfo['endTime'] == ''):
                startTime = time.mktime(time.strptime('1980-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'))
                endTime = time.mktime(time.localtime(time.time()))
            elif (searchInfo['startTime'] != '' and searchInfo['endTime'] == ''):
                startTime = time.mktime(time.strptime(searchInfo['startTime'], '%Y-%m-%d %H:%M:%S'))
                endTime = time.mktime(time.localtime(time.time()))
            elif (searchInfo['startTime'] == '' and searchInfo['endTime'] != ''):
                startTime = time.mktime(time.strptime('1980-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'))
                endTime = time.mktime(time.strptime(searchInfo['startTime'], '%Y-%m-%d %H:%M:%S'))
            else:
                startTime = time.mktime(time.strptime(searchInfo['startTime'], '%Y-%m-%d %H:%M:%S'))
                endTime = time.mktime(time.strptime(searchInfo['endTime'], '%Y-%m-%d %H:%M:%S'))

            if (float(rowValueTime) >= float(startTime)) and (float(rowValueTime) <= float(endTime)):
                betweenTimeResult = True
            else:
                betweenTimeResult = False

            if (branchResult and typeResult and nameResult and fileNameResult and betweenTimeResult):
                documents.append(rowValue)


        documnetsResult['pageSize'] = pageSize
        documnetsResult['pageNumber'] = pageNumber
        documnetsResult['total'] = len(documents)
        if (documnetsResult['total'] <= pageSize):
            documnetsResult['rows'] = documents
        else:
            documnetsResult['rows'] = documents[(pageNumber - 1) * pageSize:pageNumber * pageSize]
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(documnetsResult))
