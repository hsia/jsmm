#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import urllib
import tornado.web
import tornado_utils


@tornado_utils.bind_to(r'/members/download/([\s\S]*)')
class MemberHandlerTab(tornado.web.RequestHandler):
    def get(self, doc_path):
        filename = doc_path[16:len(doc_path)]
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + urllib.parse.quote(filename, "utf-8"))
        path = os.path.normpath(doc_path)
        with open(path, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                self.write(data)
        self.finish()
