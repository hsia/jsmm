#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import tornado.web

import tornado_utils
from commons import couch_db, get_now, make_uuid


@tornado_utils.bind_to(r'/members/search/?')
class NewMemberCollectionHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def post(self):
        obj = {
            "selector": {},
            "fields": ["_id", "_rev", "name", "gender", "birthday", "nation", "idCard", "branch", "organ", "branchTime"]
        }
        objC = obj["selector"]
        search = json.loads(self.request.body.decode('utf-8'))
        if search['name'] != '':
            objC['name'] = {"$regex": search["name"]}
        if search['gender'] != '':
            objC['gender'] = {"$regex": search["gender"]}
        if search['branchTime'] != '':
            objC['branchTime'] = {"$regex": search["branchTime"]}
        response = couch_db.post(r'/jsmm/_find/', obj)
        members = json.loads(response.body.decode('utf-8'))
        self.write(members)


@tornado_utils.bind_to(r'/members/?')
class MemberCollectionHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        '''
        通过view获取对象列表。
        '''
        response = couch_db.get(r'/jsmm/_design/members/_view/all')
        members = json.loads(response.body.decode('utf-8'))
        docs = []
        for row in members['rows']:
            docs.append(row['value'])
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(docs))

    @tornado.web.addslash
    def post(self):
        '''
        创建member对象。
        '''
        print(self.request.files)
        member = json.loads(self.request.body.decode('utf-8'))
        member['type'] = 'member'
        member['_id'] = make_uuid()
        print(member)
        couch_db.post(r'/jsmm/', member)
        response = {"success": "true"}
        self.write(response)

    def delete(self):
        '''
        删除一个或多个member对象
        '''
        memberIds = json.loads(self.request.body.decode('utf-8'))

        for memberId in memberIds:
            response = couch_db.get(r'/jsmm/%(id)s' % {'id': memberId})
            member = json.loads(response.body.decode('utf-8'))
            couch_db.delete(r'/jsmm/%(id)s?rev=%(rev)s' %
                            {'id': memberId, 'rev': member['_rev']})


@tornado_utils.bind_to(r'/members/([0-9a-f]+)')
class MemberHandler(tornado.web.RequestHandler):
    def get(self, member_id):
        '''
        获取_id为member_id的member对象。
        '''
        response = couch_db.get(r'/jsmm/%(id)s' % {"id": member_id})
        self.write(response.body.decode('utf-8'))

    def put(self, member_id):
        '''
        修改_id为member_id的member对象。
        '''
        # 获得前台对象#
        member = json.loads(self.request.body.decode('utf-8'))
        # 根据前台对象的memeber_id，查询数据库中的memeber对象#
        response = couch_db.get(r'/jsmm/%(id)s' % {'id': member_id})
        memberInDb = json.loads(response.body.decode('utf-8'))
        # 将前台数据赋予后台对象，然后将后台对象保存。#
        # 注意，如果前台传递_rev则不能将后台对象中的_rev覆盖，在index.html的编辑页面中没有包含_rev字段,因此在此处没有添加判断_rev#
        for key in memberInDb:
            if member.get(key):
                memberInDb[key] = member[key]

        memberInDb['type'] = 'member'
        memberInDb['_id'] = member_id
        couch_db.put(r'/jsmm/%(id)s' % {"id": member_id}, memberInDb)
        response = {"success": "true"}
        self.write(response)

    def delete(self, member_id):
        '''
        删除_id为member_id的member对象。
        '''
        response = couch_db.get(r'/jsmm/%(id)s' % {'id': member_id})
        member = json.loads(response.body.decode('utf-8'))
        couch_db.delete(r'/jsmm/%(id)s?rev=%(rev)s' %
                        {'id': member_id, 'rev': member['_rev']})
        response = {"success": "true"}
        self.write(response)


@tornado_utils.bind_to(r'/members/tab/([0-9a-f]+)')
class MemberHandlerTab(tornado.web.RequestHandler):
    def put(self, member_id):
        '''
        修改_id为member_id的member对象。
        '''
        memberInfo = couch_db.get(r'/jsmm/%(id)s' % {"id": member_id})
        rev = json.loads(memberInfo.body.decode('utf-8'))
        member = json.loads(self.request.body.decode('utf-8'))
        member['_id'] = member_id
        member['_rev'] = rev['_rev']
        couch_db.put(r'/jsmm/%(id)s' % {"id": member_id}, member)
        response = {"success": "true"}
        self.write(response)


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

        if ('page' not in params):
            pass
        else:
            pageNumber = params['page']

        if ('rows' not in params):
            pass
        else:
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

        if ('organName' not in params):
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

        if ('organName' not in params):
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
        if ('page' not in params):
            pass
        else:
            pageNumber = params['page']

        if ('rows' not in params):
            pass
        else:
            pageSize = params['rows']

        if ('order' not in params):
            order = True
        else:
            order = ((params['order'] == 'desc') and True or False)

        response = couch_db.post(
            '/jsmm/_design/documents/_view/all?limit=%(pageSize)s&skip=%(pageNumber)s&descending=%(order)s' % {
                'pageSize': pageSize, 'pageNumber': (pageNumber - 1) * pageSize, 'order': order},
            {"keys": [organName, "", "", "", ""]})
        documentList = json.loads(response.body.decode('utf-8'))
        documents = []
        documnetsResult = {}
        for row in documentList['rows']:
            documents.append(row['value'])
        documnetsResult['pageSize'] = pageSize
        documnetsResult['pageNumber'] = pageNumber
        documnetsResult['total'] = documentList['total_rows']
        documnetsResult['rows'] = documents
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(documnetsResult))
