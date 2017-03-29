#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json

import tornado.web
import tornado_utils

from commons import couch_db, make_uuid


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


@tornado_utils.bind_to(r'/organ/update/(.+)/(.+)/(.+)')
class OrganUpdateHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def put(self, parent_organ_id, organ_id, new_organ_name):
        """修改支社
        """
        result = {}
        response = couch_db.get(r'/jsmm/_design/organ/_view/getOrgan')
        organ_content = json.loads(response.body.decode('utf-8'))
        organ_value = (organ_content['rows'][0])['value']
        organ_bj = organ_value['organ']

        # 查找父机构,判断统计机构是否有重名的
        parent_organ = find_organ(parent_organ_id, organ_bj)
        organ = find_organ(organ_id, organ_bj)
        if parent_organ:
            # 判断是否有重复组织机构名称
            if check_same_name(new_organ_name, parent_organ[0]):
                result['success'] = False
                result['content'] = u'该机构名称已经存在，请重新输入机构名称！'
            else:
                # 查找本机构下（不包括子机构）所有社员，将社员所属支社更新为新的名称
                selector = {"selector": {"branch": {"$eq": organ[0]['text']}}}  # 此处应该改为organ_id查询
                response_member = couch_db.post(r'/jsmm/_find', selector)
                members = json.loads(response_member.body.decode('utf-8'))['docs']
                if len(members) < 1:
                    pass
                else:
                    for member in members:
                        member['branch'] = new_organ_name
                        couch_db.put(r'/jsmm/%(id)s' % {"id": member['_id']}, member)

                # 查找Organ机构,修改机构名称
                # for organ in parent_organ[0]['children']:
                #     if organ['id'] == organ_id:
                #         organ['text'] = new_organ_name
                organ[0]['text'] = new_organ_name

                couch_db.put(r'/jsmm/%(id)s' % {"id": organ_value['_id']}, organ_value)

                result["success"] = True
                result['content'] = organ_value['organ']
        else:
            result['success'] = False
            result['content'] = u'新建发生错误，请重试！'

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))


@tornado_utils.bind_to(r'/organ/merge/(.+)/(.+)/(.+)')
class OrganMergeHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def put(self, source_parent_organ_id, source_organ_id, target_organ_id):
        """
        合并支社
        :param source_parent_organ_id:
        :param source_organ_id:
        :param target_organ_id:
        :return:
        """
        result = {}
        response = couch_db.get(r'/jsmm/_design/organ/_view/getOrgan')
        organ_content = json.loads(response.body.decode('utf-8'))
        organ_value = (organ_content['rows'][0])['value']
        organ_bj = organ_value['organ']

        # 查找源机构和目标机构,判断目标机构是否有重名的
        source_parent_organ = find_organ(source_parent_organ_id, organ_bj)
        source_organ = find_organ(source_organ_id, organ_bj)
        target_organ = find_organ(target_organ_id, organ_bj)

        if check_organ_same_name(source_organ, target_organ):
            result['success'] = False
            result['content'] = u'合并的两个机构中包含重名的子机构，请检查！'
        else:
            # 更新源机构下的会员所属支社名称为目标机构名称
            selector = {"selector": {"branch": {"$eq": source_organ[0]['text']}}}
            response_member = couch_db.post(r'/jsmm/_find', selector)
            members = json.loads(response_member.body.decode('utf-8'))['docs']
            if len(members) < 1:
                pass
            else:
                for member in members:
                    member['branch'] = target_organ[0]['text']
                    couch_db.put(r'/jsmm/%(id)s' % {"id": member['_id']}, member)
            # 如果源机构下包含子机构 将其子机构添加到目标机构下的子机构中
            if "children" in source_organ[0]:
                if "children" not in target_organ[0]:
                    target_organ[0]['children'] = []
                target_organ[0]['children'].extend(source_organ[0]['children'])
            # 删除原机构
            source_parent_organ[0]['children'].remove(source_organ[0])

            couch_db.put(r'/jsmm/%(id)s' % {"id": organ_value['_id']}, organ_value)

            result["success"] = True
            result['content'] = organ_value['organ']

        self.set_header('Content-Type', 'application/json')
        self.write(result)


@tornado_utils.bind_to(r'/organ/(.+)/(.+)')
class OrganNewHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def put(self, parent_organ_id, new_organ_name):
        """新建支社
        """
        result = {};
        response = couch_db.get(r'/jsmm/_design/organ/_view/getOrgan')
        organ_content = json.loads(response.body.decode('utf-8'))
        organ_value = (organ_content['rows'][0])['value']
        organ_bj = organ_value['organ']

        # 查找parentOrgan，然后判断parentOrgan中的子机构中是否和新的子机构重名
        parent_organ = find_organ(parent_organ_id, organ_bj)
        if parent_organ:
            # 判断是否有重复组织机构名称
            if check_same_name(new_organ_name, parent_organ[0]):
                result['success'] = False
                result['content'] = u'该机构名称已经存在，请重新输入机构名称！'
            else:
                organ_new = {'id': make_uuid(), 'text': new_organ_name}
                if 'children' not in parent_organ[0]:
                    parent_organ[0]['children'] = []
                parent_organ[0]['children'].append(organ_new)

                couch_db.put(r'/jsmm/%(id)s' % {"id": organ_value['_id']}, organ_value)

                result["success"] = True
                result['content'] = organ_value['organ']
        else:
            result['success'] = False
            result['content'] = u'新建发生错误，请重试！'

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))

    def delete(self, parent_organ_id, organ_id):
        """删除支社
        """
        result = {}
        response = couch_db.get(r'/jsmm/_design/organ/_view/getOrgan')
        organ_content = json.loads(response.body.decode('utf-8'))
        organ_value = (organ_content['rows'][0])['value']
        organ_bj = organ_value['organ']

        # 查找父机构
        parent_organ = find_organ(parent_organ_id, organ_bj)
        # 查找Organ机构，然后判断Organ中是否存在子机构，如果存在子机构则不能删除
        organ = find_organ(organ_id, organ_bj)
        if organ and parent_organ:
            if 'children' in organ[0] and len((organ[0])['children']) > 0:
                result['success'] = False
                result['content'] = u'该机构下有子机构，不能删除。请将子机构删除后再删除本机构！'
            else:
                # 查找Organ机构下（包括子机构）的所有会员，如果存在则不能删除
                selector = {"selector": {"branch": {"$eq": organ[0]['text']}}}  # 此处应该改为organ_id查询
                response_member = couch_db.post(r'/jsmm/_find', selector)
                members = json.loads(response_member.body.decode('utf-8'))['docs']
                if len(members) < 1:
                    for organ in parent_organ[0]['children']:
                        if organ['id'] == organ_id:
                            parent_organ[0]['children'].remove(organ)

                    couch_db.put(r'/jsmm/%(id)s' % {"id": organ_value['_id']}, organ_value)

                    result['success'] = True
                    result['content'] = organ_value['organ']
                else:
                    result['success'] = False
                    result['content'] = u'该支社拥有社员，请将"该支社下社员删除"或者"将该支社合并到其他支社"或者"修改会员所属支社"！'
        else:
            result['success'] = False
            result['content'] = u'删除发生错误，请重试！'

        self.set_header('Content-Type', 'application/json')
        self.write(result)


# 同级别的机构名称是否重复
def check_same_name(new_organ_name, parent_organs):
    result = False
    if 'children' in parent_organs:
        for organ in parent_organs['children']:
            if new_organ_name == organ['text']:
                result = True
    return result


# 两个机构下子机构名是否重复
def check_organ_same_name(source_organ, target_organ):
    result = False
    if 'children' in source_organ[0] and 'children' in target_organ[0]:
        for source_or in source_organ[0]['children']:
            flag = False
            if flag:
                result = True
                break
            for target_or in target_organ[0]['children']:
                if source_or['text'] == target_or['text']:
                    flag = True
                    break
    return result


# 查找指定组织机构，并返回
def find_organ(organ_id, organs):
    result = []
    for organ in organs:
        if organ['id'] == organ_id:
            result.append(organ)
            return result
        if 'children' in organ:
            if len(find_organ(organ_id, organ['children'])) > 0:
                result = find_organ(organ_id, organ['children'])
        print(result)

    return result
