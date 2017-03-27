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
        tab['tab_id'] = 'custab_'+''.join(lazy_pinyin(tab['gridTitle']))
        couch_db.post(r'/jsmm/', tab)
        response = {"success": "true"}
        self.write(response)
