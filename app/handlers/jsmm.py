#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import tornado.web

import tornado_utils
from commons import couch_db, get_retire_time, make_uuid


@tornado_utils.bind_to(r'/members/search/?')
class NewMemberCollectionHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def post(self):
        keys = ['name', 'gender', 'sector', 'lost', 'stratum', 'jobLevel', 'titleLevel', 'highestEducation']
        obj = {
            "selector": {},
            "fields": ["_id", "_rev", "name", "gender", "birthday", "nation", "idCard", "branch", "organ", "branchTime"]
        }
        objC = obj["selector"]
        search = json.loads(self.request.body.decode('utf-8'))

        for key in keys:
            if key in search:
                if search[key] != '':
                    objC[key] = {'$regex': search[key]}

        if 'retireTime' in search:
            if search['retireTime'] != '':
                objC['retireTime'] = {"$lt": search["retireTime"]}

        if 'branch' in search:
            if search['branch'] != '' and search['branch'] != u'北京市' and search['branch'] != u'朝阳区':
                objC['branch'] = {"$eq": search["branch"]}

        if 'socialPositionName' in search:
            if search['socialPositionName'] != '':
                objC['social'] = {"$elemMatch": {"socialPositionName": {"$regex": search['socialPositionName']}}}

        if 'socialPositionLevel' in search:
            if search['socialPositionLevel'] != '':
                objC['social'] = {
                    "$elemMatch": {"socialPositionLevel": {"$regex": search['socialPositionLevel']}}}

        if 'formeOrganizationJob' in search:
            if search['formeOrganizationJob'] != '':
                objC['formercluboffice'] = {
                    "$elemMatch": {"formeOrganizationJob": {"$regex": search['formeOrganizationJob']}}}

        if 'formeOrganizationLevel' in search:
            if search['formeOrganizationLevel'] != '':
                objC['formercluboffice'] = {"$elemMatch": {"formeOrganizationLevel": {"$regex": search['formeOrganizationLevel']}}}

        if 'startAge' in search and 'endAge' in search:
            if search['startAge'] != '' and search['endAge']:
                objC['birthday'] = {"$gte": search['endAge'], "$lte": search['startAge']}

        objC['type'] = {"$eq": "member"}
        response = couch_db.post(r'/jsmm/_find/', obj)
        members = json.loads(response.body.decode('utf-8'))
        self.write(members)


@tornado_utils.bind_to(r'/members/?')
class MemberCollectionHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        """
        通过view获取对象列表。
        """
        if self.request.arguments == {}:
            response = couch_db.get(r'/jsmm/_design/members/_view/all')
            members = json.loads(response.body.decode('utf-8'))
            docs = []
            for row in members['rows']:
                docs.append(row['value'])
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(docs))
        else:
            startTime = self.get_argument('startTime').split('-')
            endTime = self.get_argument('endTime').split('-')
            start = '[' + ','.join(startTime) + ']'
            end = '[' + ','.join(endTime) + ']'
            memberInfo = couch_db.get(r'/jsmm/_design/members/_view/by-birthday?startkey=%(startTime)s&endkey=%(endTime)s' % {'startTime': start, 'endTime': end})
            members = json.loads(memberInfo.body.decode('utf-8'))
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
        member["retireTime"] = get_retire_time(member["birthday"], member["gender"])
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


@tornado_utils.bind_to(r'/members/tab/([0-9a-f]+)')
class MemberHandlerTab(tornado.web.RequestHandler):

    def get(self, member_id):
        '''
        通过view获取对象列表。
        '''
        response = couch_db.get(r'/jsmm/%(id)s' % {"id": member_id})
        members = json.loads(response.body.decode('utf-8'))
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(members))

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