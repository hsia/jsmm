#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Copyright sunhaitao@devTaste.com
'''

import tornado.web
from tornado.web import StaticFileHandler

from app.handlers import login_handler

registered_handlers = []


def register(pattern, handler):
    registered_handlers.append((pattern, handler))


def bind_to(pattern):
    def append(handler):
        register(pattern, handler)

    return append


def serve(port, **options):
    from tornado.web import Application
    application = Application(
        registered_handlers,
        **options
    )
    application.listen(port)
    from tornado.ioloop import IOLoop
    IOLoop.instance().start()
