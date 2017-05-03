#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import tornado.web

import tornado_utils
from pypinyin import lazy_pinyin

from app.member_importer import ErrorType
from commons import couch_db, get_retire_time, make_uuid, formatter_time


@tornado_utils.bind_to(r'/members/search/?')
class NewMemberCollectionHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):

        search = self.request.arguments;
        page_number = int((search.get('page')[0]).decode('utf-8'))
        page_size = int((search.get('rows')[0]).decode('utf-8'))
        sort_by_result = (search.get('order', [b'desc'])[0]).decode('utf-8')
        sort = (search.get('sort', [b'name'])[0]).decode('utf-8')

        # search = json.loads(self.request.body.decode('utf-8'))
        # page_number = search.get('page')
        # page_size = search.get('rows')
        # sort_by_result = search.get('order', 'desc')
        # sort = search.get('sort', 'name')
        #
        # del search['page']
        # del search['rows']
        # if 'sort' in search:
        #     del search['sort']
        # if 'order' in search:
        #     del search['order']

        keys = ['name', 'gender', 'sector', 'lost', 'stratum', 'jobLevel', 'titleLevel', 'highestEducation']
        obj = {
            "selector": {},
            "fields": ["_id", "_rev", "name", "gender", "birthday", "nation", "idCard", "branch", "organ",
                       "branchTime"],
            "sort": [{sort: sort_by_result}]
        }
        objC = obj["selector"]

        for key in keys:
            if key in search:
                if search[key] != '':
                    objC[key] = {'$regex': search[key]}

        if 'retireTime' in search:
            if search['retireTime'] != '':
                objC['retireTime'] = {"$lt": search["retireTime"]}

        if 'branch' in search:
            if search['branch'] != '' and search['branch'] != u'北京市' and search['branch'] != u'朝阳区':
                objC['branch'] = {"$eq": (search["branch"][0]).decode('utf-8')}

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
                objC['formercluboffice'] = {
                    "$elemMatch": {"formeOrganizationLevel": {"$regex": search['formeOrganizationLevel']}}}

        if 'startAge' in search and 'endAge' in search:
            if search['startAge'] != '' and search['endAge']:
                objC['birthday'] = {"$gte": search['endAge'], "$lte": search['startAge']}

        objC['type'] = {"$eq": "member"}
        # 查询总数
        response = couch_db.post(r'/jsmm/_find/', obj)
        members_count = json.loads(response.body.decode('utf-8'))

        # 获得查询分页
        obj['limit'] = page_size
        obj['skip'] = (page_number - 1) * page_size
        response_page = couch_db.post(r'/jsmm/_find/', obj)
        members_page = json.loads(response_page.body.decode('utf-8'))

        member_result = {}
        member_result['total'] = len(members_count['docs'])
        member_result['rows'] = members_page['docs']
        member_result['page_size'] = page_size
        member_result['page_number'] = page_number
        self.write(member_result)


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
            memberInfo = couch_db.get(
                r'/jsmm/_design/members/_view/by-birthday?startkey=%(startTime)s&endkey=%(endTime)s' % {
                    'startTime': start, 'endTime': end})
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
        member = json.loads(self.request.body.decode('utf-8'))
        try:
            formatter_time(member.get('birthday', ''), '%Y-%m-%d', '%Y-%m-%d')
            formatter_time(member.get('branchTime', ''), '%Y-%m-%d', '%Y-%m-%d')
            formatter_time(member.get('jobTime', ''), '%Y-%m-%d', '%Y-%m-%d')
            member['type'] = 'member'
            member['_id'] = make_uuid()
            member["retireTime"] = get_retire_time(member["birthday"], member["gender"])
            couch_db.post(r'/jsmm/', member)
            response = {"success": "true"}
        except Exception as e:
            print(e)
            response = {"success": "false", "content": ErrorType.DATAFORMATEERROR1.value}

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


@tornado_utils.bind_to(r'/members1/?')
class MemberCollectionPage1Handler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        """
        通过view获取对象列表。
        """
        param = self.request.arguments
        page_number = int((param.get('page')[0]).decode('utf-8'))
        page_size = int((param.get('rows')[0]).decode('utf-8'))
        order = (param.get('order', [b'desc'])[0]).decode('utf-8')
        sort = (param.get('sort', [b'name'])[0]).decode('utf-8')
        flag = (param.get('flag', [b''])[0]).decode('utf-8')

        member_result = {}

        if flag:
            keys = ['name', 'gender', 'sector', 'lost', 'stratum', 'jobLevel', 'jobTitle', 'titleLevel',
                    'highestEducation']
            obj = {
                "selector": {},
                "fields": ["_id", "_rev", "name", "gender", "birthday", "nation", "idCard", "branch", "organ",
                           "branchTime"],
                "sort": [{sort: order}]
            }
            objC = obj["selector"]
            objC['type'] = {"$eq": "member"}

            if 'branch' in param:
                if (param.get('branch', [b''])[0]).decode('utf-8') != '' and (param.get('branch', [b''])[0]).decode(
                        'utf-8') != u'北京市' and (param.get('branch', [b''])[0]).decode('utf-8') != u'朝阳区':
                    objC['branch'] = {"$eq": (param["branch"][0]).decode('utf-8')}

            for key in keys:
                if key in param:
                    if param.get(key, [b''])[0] != b'':
                        objC[key] = {'$regex': (param.get(key)[0]).decode("utf-8")}

            if 'retireTime' in param:
                if param.get('retireTime', [b''])[0] != b'':
                    objC['retireTime'] = {"$lt": (param.get("retireTime")[0]).decode('utf-8')}

            if 'socialPositionName' in param:
                if param.get('socialPositionName', [b''])[0] != b'':
                    objC['social'] = {
                        "$elemMatch": {
                            "socialPositionName": {"$regex": (param.get('socialPositionName')[0]).decode('utf-8')}}}

            if 'socialPositionLevel' in param:
                if param.get('socialPositionLevel', [b''])[0] != b'':
                    objC['social'] = {
                        "$elemMatch": {
                            "socialPositionLevel": {"$regex": (param.get('socialPositionLevel')[0]).decode('utf-8')}}}

            if 'formeOrganizationJob' in param:
                if param.get('formeOrganizationJob', [b''])[0] != b'':
                    objC['formercluboffice'] = {
                        "$elemMatch": {
                            "formeOrganizationJob": {"$regex": (param.get('formeOrganizationJob')[0]).decode('utf-8')}}}

            if 'formeOrganizationLevel' in param:
                if param.get('formeOrganizationLevel', [b''])[0] != b'':
                    objC['formeOrganizationLevel'] = {
                        "$elemMatch": {"formeOrganizationLevel": {
                            "$regex": (param.get('formeOrganizationLevel')[0]).decode('utf-8')}}}

            if 'startAge' in param and 'endAge' in param:
                if param.get('startAge', [b''])[0] != b'' and param.get('endAge', [b''])[0] != b'':
                    objC['birthday'] = {"$gte": (param.get('endAge')[0]).decode('utf-8'),
                                        "$lte": (param.get('startAge')[0]).decode('utf-8')}

            # 查询结果总数
            response = couch_db.post(r'/jsmm/_find/', obj)
            members_count = json.loads(response.body.decode('utf-8'))
            # 查询分页数据
            obj['limit'] = page_size
            obj['skip'] = (page_number - 1) * page_size
            response_page = couch_db.post(r'/jsmm/_find/', obj)
            members_page = json.loads(response_page.body.decode('utf-8'))

            member_result['total'] = len(members_count['docs'])
            member_result['rows'] = members_page['docs']
        else:
            if order == 'asc':
                sort_by_result = False
            else:
                sort_by_result = True

            if sort == 'gender':
                views = 'sort-by-gender'
            elif sort == 'birthday':
                views = 'sort-by-birthday'
            elif sort == 'nation':
                views = 'sort-by-nation'
            elif sort == 'idCard':
                views = 'sort-by-idCard'
            elif sort == 'branch':
                views = 'sort-by-branch'
            elif sort == 'organ':
                views = 'sort-by-organ'
            elif sort == 'branchTime':
                views = 'sort-by-branchTime'
            else:
                views = 'sort-by-name'
            response = couch_db.get(
                r'/jsmm/_design/members/_view/%(views)s?limit=%(page_size)s&skip=%(page_number)s&descending=%(sort_by_result)s' % {
                    'views': views,
                    'page_size': page_size, 'page_number': (page_number - 1) * page_size,
                    'sort_by_result': sort_by_result})
            members = json.loads(response.body.decode('utf-8'))
            member_rows = members.get('rows')

            result = []
            for member in member_rows:
                result.append(member.get('value'))

            member_result['total'] = members['total_rows']
            member_result['rows'] = result

        member_result['page_size'] = page_size
        member_result['page_number'] = page_number

        self.set_header('Content-Type', 'application/json')
        self.write(member_result)


@tornado_utils.bind_to(r'/members2/?')
class MemberCollectionPage2Handler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        """
        通过view获取对象列表。
        """
        param = self.request.arguments
        page_number = int((param.get('page')[0]).decode('utf-8'))
        page_size = int((param.get('rows')[0]).decode('utf-8'))
        order = (param.get('order', [b'desc'])[0]).decode('utf-8')
        sort = (param.get('sort', [b'name'])[0]).decode('utf-8')
        flag = (param.get('flag', [b''])[0]).decode('utf-8')

        member_result = {}

        if flag:
            keys = ['name', 'gender', 'sector', 'lost', 'stratum', 'jobLevel', 'jobTitle', 'titleLevel',
                    'highestEducation']
            obj = {
                "selector": {},
                "fields": ["_id", "_rev", "name", "gender", "birthday", "nation", "idCard", "branch", "organ",
                           "branchTime"],
                "limit": 10000
            }
            objC = obj["selector"]
            objC['type'] = {"$eq": "member"}

            if 'branch' in param:
                if (param.get('branch', [b''])[0]).decode('utf-8') != '' and (param.get('branch', [b''])[0]).decode(
                        'utf-8') != u'北京市' and (param.get('branch', [b''])[0]).decode('utf-8') != u'朝阳区':
                    objC['branch'] = {"$eq": (param["branch"][0]).decode('utf-8')}

            for key in keys:
                if key in param:
                    if param.get(key, [b''])[0] != b'':
                        objC[key] = {'$regex': (param.get(key)[0]).decode("utf-8")}

            if 'retireTime' in param:
                if param.get('retireTime', [b''])[0] != b'':
                    objC['retireTime'] = {"$lt": (param.get("retireTime")[0]).decode('utf-8')}

            if 'socialPositionName' in param:
                if param.get('socialPositionName', [b''])[0] != b'':
                    objC['social'] = {
                        "$elemMatch": {
                            "socialPositionName": {"$regex": (param.get('socialPositionName')[0]).decode('utf-8')}}}

            if 'socialPositionLevel' in param:
                if param.get('socialPositionLevel', [b''])[0] != b'':
                    objC['social'] = {
                        "$elemMatch": {
                            "socialPositionLevel": {"$regex": (param.get('socialPositionLevel')[0]).decode('utf-8')}}}

            if 'formeOrganizationJob' in param:
                if param.get('formeOrganizationJob', [b''])[0] != b'':
                    objC['formercluboffice'] = {
                        "$elemMatch": {
                            "formeOrganizationJob": {"$regex": (param.get('formeOrganizationJob')[0]).decode('utf-8')}}}

            if 'formeOrganizationLevel' in param:
                if param.get('formeOrganizationLevel', [b''])[0] != b'':
                    objC['formeOrganizationLevel'] = {
                        "$elemMatch": {"formeOrganizationLevel": {
                            "$regex": (param.get('formeOrganizationLevel')[0]).decode('utf-8')}}}

            if 'startAge' in param and 'endAge' in param:
                if param.get('startAge', [b''])[0] != b'' and param.get('endAge', [b''])[0] != b'':
                    objC['birthday'] = {"$gte": (param.get('endAge')[0]).decode('utf-8'),
                                        "$lte": (param.get('startAge')[0]).decode('utf-8')}

            # 查询结果总数
            response = couch_db.post(r'/jsmm/_find/', obj)
            members = json.loads(response.body.decode('utf-8'))
            # 查询分页数据
            # obj['limit'] = page_size
            # obj['skip'] = (page_number - 1) * page_size
            # response_page = couch_db.post(r'/jsmm/_find/', obj)
            # members_page = json.loads(response_page.body.decode('utf-8'))

            # member_result['total'] = len(members_count['docs'])
            # member_result['rows'] = members_page['docs']
            member_result = members.get('docs')
        else:
            if order == 'asc':
                sort_by_result = False
            else:
                sort_by_result = True

            # if sort == 'gender':
            #     views = 'sort-by-gender'
            # elif sort == 'birthday':
            #     views = 'sort-by-birthday'
            # elif sort == 'nation':
            #     views = 'sort-by-nation'
            # elif sort == 'idCard':
            #     views = 'sort-by-idCard'
            # elif sort == 'branch':
            #     views = 'sort-by-branch'
            # elif sort == 'organ':
            #     views = 'sort-by-organ'
            # elif sort == 'branchTime':
            #     views = 'sort-by-branchTime'
            # else:
            #     views = 'sort-by-name'
            response = couch_db.get(
                r'/jsmm/_design/members/_view/sort-by-name?descending=%(sort_by_result)s' % {
                    'sort_by_result': sort_by_result})
            members = json.loads(response.body.decode('utf-8'))
            member_rows = members.get('rows')

            result = []
            for member in member_rows:
                result.append(member.get('value'))

            member_result = result

        member_result.sort(key=lambda k: lazy_pinyin(k.get('name')))

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(member_result))
