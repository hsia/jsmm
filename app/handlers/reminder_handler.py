#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import tornado.web
import tornado_utils
import re
from commons import couch_db


@tornado_utils.bind_to(r'/members/reminder/(.*)')
class reminderRetireHandler(tornado.web.RequestHandler):

    def get(self, retire_time):
        """
            退休提醒
        """
        if re.match("([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8])))", retire_time, flags=0):
            obj = {
                "selector": {
                    "retireTime": {
                        "$lt": retire_time
                    }
                },
                "fields": ["_id", "_rev", "name", "gender", "birthday", "nation", "idCard", "branch", "organ", "branchTime"]
            }
            response = couch_db.post(r'/jsmm/_find/', obj)
            members = json.loads(response.body.decode('utf-8'))
            self.write(members)