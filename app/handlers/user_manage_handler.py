#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json

import tornado.web
import tornado_utils

from commons import couch_db


@tornado_utils.bind_to(r'/user/?')
class UserManageHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.addslash
    def post(self):
        # user_info = {'userName': self.get_argument('userName'), 'oldPassword': self.get_argument('oldPassword'),
        #              'newPassword': self.get_argument('newPassword'),
        #              'newPasswordSecond': self.get_argument('newPasswordSecond')}
        user_info = json.loads(self.request.body.decode("utf-8"))
        result = {}

        # 验证旧密码是否一致
        selector = {
            "selector": {"$and": [
                {"type": {"$eq": "user"}},
                {"username": {"$eq": user_info['userName']}},
            ]},
            "fields": ["_id", "_rev", "type", "username", "password"]
        }

        user_response = couch_db.post(r'/jsmm/_find/', selector)
        user_info_indbs = (json.loads(user_response.body.decode('utf-8'))['docs'])
        if len(user_info_indbs) > 0:
            user_info_indb = user_info_indbs[0]
            if user_info_indb['password'] == user_info['oldPassword']:
                # 验证两次新密码是否一致
                if user_info['newPassword'] == user_info['newPasswordSecond']:
                    # 更新密码
                    user_info_indb['password'] = user_info['newPassword']
                    couch_db.put(r'/jsmm/%(id)s' % {"id": user_info_indb['_id']}, user_info_indb)
                    result = {"success": True}
                else:
                    result = {"success": False, "content": "两次新密码不一致，请重新输入！"}
                    # 修改密码
            else:
                result = {"success": False, "content": "当前用户的密码不正确，请重新输入！"}
        else:
            result = {"success": False, "content": "当前用户修改密码发生错误！"}

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))
