#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import tornado.web
import tornado_utils
from pypinyin import lazy_pinyin

from commons import couch_db, make_uuid


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
        print(self.request.files)
        tab = json.loads(self.request.body.decode('utf-8'))
        tab['type'] = 'tab'
        tab['_id'] = make_uuid()
        tab['tab_id'] = 'custab_' + ''.join(lazy_pinyin(tab['gridTitle']))

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

    def delete(self, tab_name):
        # 判断自定义tab名称是否已经存在
        tab_id = 'custab_' + ''.join(lazy_pinyin(tab_name))
        tab_selector = {
            "selector": {
                "tab_id": {
                    "$eq": tab_id
                }
            }
        }

        response = couch_db.post(r'/jsmm/_find/', tab_selector)
        tabs = json.loads(response.body.decode('utf-8'))
        tab_list = tabs["docs"]
        # 判断是否存在名称为tab_name的tab
        if len(tab_list) <= 0:
            result = {"success": False, "content": u"该tab名称不存在，请重新输入！"}
        else:
            tab_target = tab_list[0]
            # 刪除member中的tab信息
            member_selector = {
                "selector": {
                    "$and": [
                        {"type": {
                            "$eq": "member"
                        }
                        },
                        {tab_id: {
                            "$ne": "null"
                        }
                        }
                    ]
                }
            }

            member_response = couch_db.post(r'/jsmm/_find/', member_selector)
            member_list = json.loads(member_response.body.decode('utf-8'))["docs"]
            for member in member_list:
                del member[tab_id]
                couch_db.put(r'/jsmm/%(id)s' % {"id": member["_id"]}, member)

            # 刪除tab
            couch_db.delete(r'/jsmm/%(id)s?rev=%(rev)s' %
                            {'id': tab_target["_id"], 'rev': tab_target["_rev"]})
            result = {"success": True}
        self.write(result)
