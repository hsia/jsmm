#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Copyright sunhaitao@devTaste.com
'''

import tornado.web
from tornado.web import StaticFileHandler

registered_handlers = []


def register(pattern, handler):
    registered_handlers.append((pattern, handler))


def bind_to(pattern):
  def append(handler):
    register(pattern, handler)
  return append

static_file_dir = 'www'
default_filename = 'index.html'

def serve(port, **options):
    from tornado.web import Application
    application = Application(
        registered_handlers + [
          (
            r'/(.*)',
            StaticFileHandler,
            {
              'path': static_file_dir,
              'default_filename': default_filename
            }
          )
        ],
        **options
    )
    application.listen(port)
    from tornado.ioloop import IOLoop
    IOLoop.instance().start()
