#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

import time
import tornado

from commons import couch_db


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")


class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        result = {}

        username = self.get_argument('username', None)
        password = self.get_argument('password', None)

        # user = json.loads(self.request.body.decode('utf-8'))
        # username = user["username"]
        # password = user["password"]

        if username and password:
            selector = {
                "selector": {"$and": [
                    {"type": {"$eq": "user"}},
                    {"username": {"$eq": username}},
                    {"password": {"$eq": password}}
                ]},
                "fields": ["_id", "_rev", "username", "password"]
            }

            user_response = couch_db.post(r'/jsmm/_find/', selector)
            response_content = json.loads(user_response.body.decode('utf-8'))
            user_in_db = response_content['docs']
            if len(user_in_db) > 0:
                self.set_secure_cookie("username", username, expires_days=None, expires=time.time() + 36000)
                # self.redirect("/")
                result = {"success": True}
            else:
                result = {"success": False}
        else:
            result = {"success": False}

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))


class WelcomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('index.html', user=self.current_user)


class LogoutHandler(BaseHandler):
    def get(self):
        # if (self.get_argument("logout", None)):
        self.clear_cookie("username")
        self.redirect("/")
