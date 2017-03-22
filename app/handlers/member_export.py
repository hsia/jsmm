#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import urllib
from io import BytesIO

import time
import tornado.web
import tornado_utils
import xlwt

from commons import couch_db


@tornado_utils.bind_to(r'/member/simpleinfo/?')
class membersExport(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        selector = {
            "selector": {
                "type": {"$eq": "member"}
            },
            "fields": ["name", "gender", "highestEducation", "jobTitle", "duty", "mobile",
                       "email", "companyName", "companyTel", "commAddress", "commPost"]
        }
        response = couch_db.post(r'/jsmm/_find/', selector)
        membersSimpleInfo = json.loads(response.body.decode('utf-8'))["docs"]

        titles = {u'姓名': 10, u'性别': 6, u'最高学历': 10, u'职称': 12, u'职务': 12, u'移动电话': 13, u'邮箱': 25, u'单位名称': 26,
                  u'单位电话': 15, u'单位地址': 40, u'邮编': 10}

        style_heading = xlwt.easyxf("""
                font:
                    name 微软雅黑,
                    colour_index black,
                    bold on,
                    height 200;
                align:
                    wrap off,
                    vert center,
                    horiz centre;
                pattern:
                    pattern solid,
                    fore-colour 22;
                borders:
                    left THIN,
                    right THIN,
                    top THIN,
                    bottom THIN;
                """)
        style_data = xlwt.easyxf("""
                        font:
                            name 微软雅黑,
                            colour_index black,
                            bold off,
                            height 180;
                        align:
                            wrap off,
                            vert center,
                            horiz left;
                        pattern:
                            pattern solid,
                            fore-colour 1;
                        borders:
                            left thin,
                            right thin,
                            top thin,
                            bottom thin;
                        """)

        workBook = xlwt.Workbook(encoding='utf-8')
        workSheet = workBook.add_sheet('会员信息简表')

        column = 0
        row = 0
        for title in titles:
            workSheet.write(row, column, title, style_heading)
            workSheet.col(column).width = titles[title] * 256
            column += 1

        if len(membersSimpleInfo) > 1:
            row = 1
            for member in membersSimpleInfo:
                column = 0
                for key in member:
                    workSheet.write(row, column, member[key], style_data)
                    column += 1
                row += 1
        else:
            pass

        sio = BytesIO()
        workBook.save(sio)
        self.set_header('Content-Type', 'application/vnd.ms-excel')
        self.set_header('Content-Disposition', 'attachment; filename=' + urllib.parse.quote('会员信息简表.xls', "utf-8"))
        self.write(sio.getvalue())
        self.finish()
