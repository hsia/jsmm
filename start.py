#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from tornado import web

import commons

if __name__ == "__main__":
    print("Starting...")
    import tornado_utils
    from handlers import *
    from member_importer import import_info

    tornado_utils.registered_handlers += [
        (r'/members/upload/?', member_upload.UploadHandler, dict(callback=import_info)),
        (r'/image/upload/?', member_image.UploadImage, dict(callback=member_image.imageCallBack)),
        (r'/', login_handler.WelcomeHandler),
        (r'/login', login_handler.LoginHandler),
        (r'/logout', login_handler.LogoutHandler),
        # ,(r'/doc/upload/?', member_doc.UploadDoc, dict(callback=member_doc.docCallBack))
    ]
    settings = {
        'template_path': os.path.join(os.path.dirname(__file__), 'www/templates'),
        'static_path': os.path.join(os.path.dirname(__file__), 'www/statics'),
        'login_url': '/login',
        'cookie_secret': "2379874hsdhf0234990sdhsaiuofyasop977djdj",
        'debug': True
    }
    tornado_utils.serve(2063, **settings)
