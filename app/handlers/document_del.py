#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import tornado.web
import tornado_utils
from commons import couch_db


@tornado_utils.bind_to(r'/members/del/')
class MemberDocsDel(tornado.web.RequestHandler):
    def post(self):
        obj = json.loads(self.request.body.decode('utf-8'))
        response = couch_db.get(r'/jsmm/%(id)s' % {"id": obj["id"]})
        member = json.loads(response.body.decode('utf-8'))
        doctype = obj['doc_type']
        member[doctype].remove(obj['rowData'])
        couch_db.put(r'/jsmm/%(id)s' % {"id": obj['id']}, member)
        path = os.path.normpath(obj['file_url'])
        os.remove(path)