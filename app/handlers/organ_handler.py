#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json

import tornado.web

from commons import couch_db
from lib import tornado_utils


@tornado_utils.bind_to(r'/organ/?')
class OrganHandler(tornado.web.RequestHandler):
    """组织机构处理类

    URL: '/organ
    """

    def data_received(self, chunk):
        pass

    def get(self):
        """获取组织机构信息
        """
        response = couch_db.get(r'/jsmm/_design/organ/_view/getOrgan')
        organ_content = json.loads(response.body.decode('utf-8'))
        organ_row = organ_content['rows'][0]
        organ_value = organ_row['value']
        organ = organ_value['organ']

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(organ))

    # 支社的增删改操作
    def post(self):
        flag = self.get_argument('flag')

        result = {};
        response = couch_db.get(r'/jsmm/_design/organ/_view/getOrgan')
        organ_content = json.loads(response.body.decode('utf-8'))
        organ_row = organ_content['rows'][0]
        organ_value = organ_row['value']
        organ_cy = (((organ_value['organ'])[0])['children'])[0]

        if flag == 'add':
            # 添加支社
            new_organ_value = self.get_argument('organName')
            if new_organ_value:
                organ = {'id': new_organ_value, 'text': new_organ_value}

                if 'children' not in organ_cy:
                    organ_cy['children'] = list()

                # 判断是否有重名的
                if organ in organ_cy['children']:
                    result['success'] = False
                    result['content'] = u'支社已经存在，请重新输入支社名称！'
                else:
                    organ_cy['children'].append(organ)
                    couch_db.put(r'/jsmm/%(id)s' % {"id": organ_value['_id']}, organ_value)

                    result["success"] = True
                    result['content'] = organ_value['organ']
            else:
                result['success'] = False
                result['content'] = u'支社名称不能为空，请重新输入支社名称！'
        elif flag == 'edit':
            # 编辑支社
            new_organ_value = self.get_argument('organName')
            organ_id = self.get_argument('organId')
            if new_organ_value and organ_id:
                organ = {'id': new_organ_value, 'text': new_organ_value}
                # 判断修改后的机构是否重名
                if organ in organ_cy['children']:
                    result['success'] = False
                    result['content'] = u'支社已经存在，请重新输入支社名称！'
                else:
                    selector = {"selector": {"branch": {"$eq": organ_id}}}
                    response_member = couch_db.post(r'/jsmm/_find', selector)
                    members = json.loads(response_member.body.decode('utf-8'))['docs']
                    if len(members) < 1:
                        pass
                    else:
                        for member in members:
                            member['branch'] = new_organ_value
                            couch_db.put(r'/jsmm/%(id)s' % {"id": member['_id']}, member)

                    for organ in organ_cy['children']:
                        if organ['id'] == organ_id:
                            organ['text'] = new_organ_value
                            organ['id'] = new_organ_value
                    couch_db.put(r'/jsmm/%(id)s' % {"id": organ_value['_id']}, organ_value)

                    result['success'] = True
                    result['content'] = organ_value['organ']
            else:
                result['success'] = False
                result['content'] = u'支社名称不能为空，请重新输入支社名称！'
        elif flag == 'merge':
            # 合并支社
            source_organ_id = self.get_argument('organId')
            target_organ_id = self.get_argument('organName')

            if source_organ_id and target_organ_id:
                selector = {"selector": {"branch": {"$eq": source_organ_id}}}
                response_member = couch_db.post(r'/jsmm/_find', selector)
                members = json.loads(response_member.body.decode('utf-8'))['docs']
                if len(members) < 1:
                    pass
                else:
                    for member in members:
                        member['branch'] = target_organ_id
                        couch_db.put(r'/jsmm/%(id)s' % {"id": member['_id']}, member)

                for organ in organ_cy['children']:
                    if organ['id'] == source_organ_id:
                        organ_cy['children'].remove(organ)

                couch_db.put(r'/jsmm/%(id)s' % {"id": organ_value['_id']}, organ_value)

                result = organ_value['organ']
            else:
                result = []
        elif flag == 'delete':
            # 删除支社
            organ_id = self.get_argument('')

            selector = {"selector": {"branch": {"$eq": organ_id}}}
            response_member = couch_db.post(r'/jsmm/_find', selector)
            members = json.loads(response_member.body.decode('utf-8'))['docs']
            if len(members) < 1:
                for organ in organ_cy['children']:
                    if organ['id'] == organ_id:
                        organ_cy['children'].remove(organ)

                couch_db.put(r'/jsmm/%(id)s' % {"id": organ_value['_id']}, organ_value)

                result['success'] = True
                result['content'] = organ_value['organ']
            else:
                result['success'] = False
                result['content'] = u'该支社拥有社员，请将"该支社下社员删除"或者"将该支社合并到其他支社"或者"修改会员所属支社"！'
        else:
            result = {"success": False, 'content': "操作错误"}

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))


@tornado_utils.bind_to(r'/organ/update/(.+)/(.+)')
class OrganUpdateHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def put(self, organ_id, new_organ_value):
        """修改支社
        """
        result = {}
        response = couch_db.get(r'/jsmm/_design/organ/_view/getOrgan')
        organ_content = json.loads(response.body.decode('utf-8'))
        organ_row = organ_content['rows'][0]
        organ_value = organ_row['value']
        organ_cy = (((organ_value['organ'])[0])['children'])[0]

        organ = {'id': new_organ_value, 'text': new_organ_value}
        # 判断修改后的机构是否重名
        if organ in organ_cy['children']:
            result['success'] = False
            result['content'] = u'支社已经存在，请重新输入支社名称！'
        else:
            selector = {"selector": {"branch": {"$eq": organ_id}}}
            response_member = couch_db.post(r'/jsmm/_find', selector)
            members = json.loads(response_member.body.decode('utf-8'))['docs']
            if len(members) < 1:
                pass
            else:
                for member in members:
                    member['branch'] = new_organ_value
                    couch_db.put(r'/jsmm/%(id)s' % {"id": member['_id']}, member)

            for organ in organ_cy['children']:
                if organ['id'] == organ_id:
                    organ['text'] = new_organ_value
                    organ['id'] = new_organ_value
            couch_db.put(r'/jsmm/%(id)s' % {"id": organ_value['_id']}, organ_value)

            result['success'] = True
            result['content'] = organ_value['organ']

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))


@tornado_utils.bind_to(r'/organ/merge/(.+)/(.+)')
class OrganMergeHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def put(self, source_organ_id, target_organ_id):
        """
        合并支社
        :param source_organ_id:
        :param target_organ_id:
        :return:
        """
        response = couch_db.get(r'/jsmm/_design/organ/_view/getOrgan')
        organ_content = json.loads(response.body.decode('utf-8'))
        organ_row = organ_content['rows'][0]
        organ_value = organ_row['value']
        organ_cy = (((organ_value['organ'])[0])['children'])[0]

        selector = {"selector": {"branch": {"$eq": source_organ_id}}}
        response_member = couch_db.post(r'/jsmm/_find', selector)
        members = json.loads(response_member.body.decode('utf-8'))['docs']
        if len(members) < 1:
            pass
        else:
            for member in members:
                member['branch'] = target_organ_id
                couch_db.put(r'/jsmm/%(id)s' % {"id": member['_id']}, member)

        for organ in organ_cy['children']:
            if organ['id'] == source_organ_id:
                organ_cy['children'].remove(organ)

        couch_db.put(r'/jsmm/%(id)s' % {"id": organ_value['_id']}, organ_value)

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(organ_value['organ']))


@tornado_utils.bind_to(r'/organ/(.+)')
class OrganOperationHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def put(self, new_organ_value):
        """新建支社
        """
        result = {}
        response = couch_db.get(r'/jsmm/_design/organ/_view/getOrgan')
        organ_content = json.loads(response.body.decode('utf-8'))
        organ_row = organ_content['rows'][0]
        organ_value = organ_row['value']
        organ_cy = (((organ_value['organ'])[0])['children'])[0]

        organ = {'id': new_organ_value, 'text': new_organ_value}

        if 'children' not in organ_cy:
            organ_cy['children'] = list()

        # 判断是否有重名的
        if organ in organ_cy['children']:
            result['success'] = False
            result['content'] = u'支社已经存在，请重新输入支社名称！'
        else:
            organ_cy['children'].append(organ)
            couch_db.put(r'/jsmm/%(id)s' % {"id": organ_value['_id']}, organ_value)

            result["success"] = True
            result['content'] = organ_value['organ']

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))

    def delete(self, organ_id):
        """删除支社
        """
        result = {}
        response = couch_db.get(r'/jsmm/_design/organ/_view/getOrgan')
        organ_content = json.loads(response.body.decode('utf-8'))
        organ_row = organ_content['rows'][0]
        organ_value = organ_row['value']
        organ_cy = (((organ_value['organ'])[0])['children'])[0]

        selector = {"selector": {"branch": {"$eq": organ_id}}}
        response_member = couch_db.post(r'/jsmm/_find', selector)
        members = json.loads(response_member.body.decode('utf-8'))['docs']
        if len(members) < 1:
            for organ in organ_cy['children']:
                if organ['id'] == organ_id:
                    organ_cy['children'].remove(organ)

            couch_db.put(r'/jsmm/%(id)s' % {"id": organ_value['_id']}, organ_value)

            result['success'] = True
            result['content'] = organ_value['organ']
        else:
            result['success'] = False
            result['content'] = u'该支社拥有社员，请将"该支社下社员删除"或者"将该支社合并到其他支社"或者"修改会员所属支社"！'

        self.set_header('Content-Type', 'application/json')
        self.write(result)
