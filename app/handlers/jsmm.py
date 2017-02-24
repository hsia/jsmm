#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import tornado.web

import tornado_utils
from commons import couch_db, get_now, make_uuid


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
        member = json.loads(self.request.body.decode('utf-8'))
        member['type'] = 'member'
        member['_id'] = member_id
        couch_db.put(r'/jsmm/%(id)s' % {"id": member_id}, member)
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
class MemberHandlerTab(tornado.web.RequestHandler):
    def get(self):
        '''
        修改_id为member_id的member对象。
        '''
        response = couch_db.get(r'/jsmm/_design/documentList/_view/documents')
        doucmentList = json.loads(response.body.decode('utf-8'))
        documents = []
        for row in doucmentList['rows']:
            documents.append(row['value'])
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(documents))
