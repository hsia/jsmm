#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import os.path
import time
import uuid

import tornado.web

import tornado_utils
from commons import couch_db, make_uuid


@tornado_utils.bind_to(r'/document/([0-9a-f]+)')
class DocumentHandler(tornado.web.RequestHandler):
    """文档处理类

    URL: '/document/<document_id>
    """

    def get(self, document_id):
        """获取文档信息
        """
        self.write(couch_db.get(r'/jsmm/%(document_id)s' %
                                {'document_id': document_id}))

    def put(self, document_id):
        """修改文档信息
        """
        pass

    def delete(self, document_id):
        """删除文档
        """
        pass
