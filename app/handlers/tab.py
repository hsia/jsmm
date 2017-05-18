#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import tornado.web
from pypinyin import lazy_pinyin

from commons import couch_db, make_uuid
from lib import tornado_utils


@tornado_utils.bind_to(r'/tab/?')
class TabCollectionHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        """
        通过find获取对象列表。
        """

        obj = {
            "selector": {
                "type": {
                    "$eq": "tab"
                }
            }
        }

        response = couch_db.post(r'/jsmm/_find/', obj)
        tab = json.loads(response.body.decode('utf-8'))
        self.write(tab)

    @tornado.web.addslash
    def post(self):
        """
        创建tab对象。
        """
        tab = json.loads(self.request.body.decode('utf-8'))
        if tab.get('columns', []):
            for column in tab.get('columns'):
                if column.get('editor', ''):
                    pass
                else:
                    column['editor'] = 'textbox'
        tab['type'] = 'tab'
        tab['_id'] = make_uuid()
        tab['tab_id'] = 'custab_' + ''.join(lazy_pinyin(tab['gridTitle']))

        for column in tab.get('columns', []):
            column['col_id'] = make_uuid()
            column['field'] = column['col_id']

        # 判断自定义tab名称是否已经存在
        obj = {
            "selector": {
                "tab_id": {
                    "$eq": tab['tab_id']
                }
            }
        }

        response = couch_db.post(r'/jsmm/_find/', obj)
        tabs = json.loads(response.body.decode('utf-8'))
        if len(tabs["docs"]) > 0:
            result = {"success": False, "content": u"该tab名称已经存在，请重新输入！"}
        else:
            couch_db.post(r'/jsmm/', tab)
            result = {"success": True}
        self.write(result)


@tornado_utils.bind_to(r'/tab/(.+)')
class TabDeleteHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def delete(self, tab_id):
        # 判断自定义tab名称是否已经存在
        response = couch_db.get(r'/jsmm/%(id)s' % {'id': tab_id})
        tab = json.loads(response.body.decode('utf-8'))
        # 判断是否存在名称为tab_name的tab

        if tab:
            tab_column = 'custab_' + tab['gridTitle']
            # 刪除member中的tab信息
            member_selector = {
                "selector": {
                    "$and": [
                        {"type": {"$eq": "member"}},
                        {tab_column: {"$ne": "null"}}
                    ]
                }
            }

            member_response = couch_db.post(r'/jsmm/_find/', member_selector)
            member_list = json.loads(member_response.body.decode('utf-8'))["docs"]
            for member in member_list:
                del member[tab_column]
                couch_db.put(r'/jsmm/%(id)s' % {"id": member["_id"]}, member)

            # 刪除tab
            couch_db.delete(r'/jsmm/%(id)s?rev=%(rev)s' %
                            {'id': tab["_id"], 'rev': tab["_rev"]})
            result = {"success": True}
        else:
            result = {"success": False, "content": u"该tab不存在，请重新选择！"}
        self.write(result)


@tornado_utils.bind_to(r'/tabcombtree/?')
class TabComtreeHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        response = couch_db.get(r'/jsmm/_design/tab/_view/tab-combtree')
        tabs = json.loads(response.body.decode('utf-8')).get('rows', [])
        trees = []
        for tab in tabs:
            trees.append(tab['value'])

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(trees))


@tornado_utils.bind_to(r'/tabcombtree/(.+)')
class TabInfoHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self, tab_id):
        response = couch_db.get(r'/jsmm/%(tab_id)s' % {'tab_id': tab_id})
        tab_info = json.loads(response.body.decode('utf-8'))

        self.set_header('Content-Type', 'application/json')
        self.write(tab_info)


@tornado_utils.bind_to(r'/tabedit/?')
class TabEditHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def post(self):
        """
        更新tab对象。
        """
        tab = json.loads(self.request.body.decode('utf-8'))
        tab['type'] = 'tab'
        tab['tab_id'] = 'custab_' + ''.join(lazy_pinyin(tab['gridTitle']))

        for column in tab.get('columns', []):
            if 'col_id' not in column:
                column['col_id'] = make_uuid()
                column['field'] = column['col_id']

        # 判断自定义tab名称是否已经存在
        obj = {
            "selector": {
                "tab_id": {
                    "$eq": tab['tab_id']
                }
            }
        }

        response = couch_db.post(r'/jsmm/_find/', obj)
        tabs = json.loads(response.body.decode('utf-8'))
        if len(tabs["docs"]) > 1:
            result = {"success": False, "content": u"该tab名称已经存在，请重新输入！"}
        else:
            # 更新tab信息
            tab['_rev'] = tabs["docs"][0]['_rev']
            couch_db.put(r'/jsmm/%(id)s' % {'id': tab['_id']}, tab)

            '''
            根据更新后的tab，修改member中的数据,主要是处理tab删除行的情况
            '''
            # 经修改后的列名取出
            columns_name = []
            for column in tab['columns']:
                columns_name.append(column.get('field'))

            member_selector = {
                "selector": {
                    "$and": [
                        {"type": {"$eq": "member"}},
                        {tab['tab_id']: {"$ne": "null"}}
                    ]
                }
            }

            response = couch_db.post('/jsmm/_find', member_selector)
            members_list = json.loads(response.body.decode('utf-8')).get('docs')

            if members_list:
                for member in members_list:
                    custom_tab = member.get(tab['tab_id'])
                    for custom_columns in custom_tab:
                        keys = list(custom_columns.keys())
                        for key in keys:
                            if key not in columns_name:
                                del custom_columns[key]

                    couch_db.put(r'/jsmm/%(id)s' % {'id': member['_id']}, member)

            result = {"success": True}
        self.write(result)
