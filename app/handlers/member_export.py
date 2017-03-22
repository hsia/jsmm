#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import urllib
from commons import couch_db
from io import BytesIO
import json

import time
import tornado.web
import tornado_utils
import xlwt

@tornado_utils.bind_to(r'/member/export/([0-9a-f]+)')
class memberInfoExport(tornado.web.RequestHandler):
    def get(self, member_id):
        response = couch_db.get(r'/jsmm/%(id)s' % {"id": member_id})
        member = json.loads(response.body.decode('utf-8'))
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

        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 22
        style = xlwt.XFStyle()
        style.pattern = pattern
        style.font.height = 240
        style.font.name = '宋体'

        memberInfoStyle = xlwt.XFStyle()
        memberInfoStyle.font.name = '宋体'
        memberInfoStyle.font.height = 240
        memberInfoStyle.font.width = 230
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

        wb = xlwt.Workbook()
        ws = wb.add_sheet(member['name'] + '的信息', cell_overwrite_ok=True)
        workBook = xlwt.Workbook(encoding='utf-8')
        workSheet = workBook.add_sheet('会员信息简表')

        for c in range(0, 10):
            ws.col(c).width = 4000

        ws.write_merge(0, 0, 0, 9, u'基本信息', style)
        ws.write(1, 0, u'姓名', memberInfoStyle)
        ws.write(1, 2, u'性别', memberInfoStyle)
        ws.write(1, 4, u'籍贯', memberInfoStyle)
        ws.write(2, 0, u'民族', memberInfoStyle)
        ws.write(2, 2, u'出生地', memberInfoStyle)
        ws.write(2, 4, u'出生年月日', memberInfoStyle)
        ws.write(3, 0, u'外文姓名', memberInfoStyle)
        ws.write(3, 3, u'曾用名', memberInfoStyle)
        ws.write(4, 0, u'健康状态', memberInfoStyle)
        ws.write(4, 3, u'婚姻状态', memberInfoStyle)
        ws.write(5, 0, u'所属支社', memberInfoStyle)
        ws.write(5, 3, u'所属基层组织', memberInfoStyle)
        ws.write(6, 0, u'入社时间', memberInfoStyle)
        ws.write(6, 3, u'党派交叉', memberInfoStyle)
        ws.write(7, 0, u'单位名称', memberInfoStyle)
        ws.write(7, 3, u'工作部门', memberInfoStyle)
        ws.write(8, 0, u'职务', memberInfoStyle)
        ws.write(8, 3, u'职称', memberInfoStyle)
        ws.write(9, 0, u'学术职务', memberInfoStyle)
        ws.write(9, 3, u'参加工作时间', memberInfoStyle)
        ws.write_merge(9, 9, 6, 7, u'是否办理退休', memberInfoStyle)
        ws.write(10, 0, u'公民身份证号', memberInfoStyle)
        ws.write(10, 3, u'有效证件类别', memberInfoStyle)
        ws.write_merge(10, 10, 6, 7, u'证件号码', memberInfoStyle)
        ws.write(11, 0, u'家庭地址', memberInfoStyle)
        ws.write(11, 4, u'邮编', memberInfoStyle)
        ws.write(12, 0, u'单位地址', memberInfoStyle)
        ws.write(12, 4, u'邮编', memberInfoStyle)
        ws.write(13, 0, u'通信地址', memberInfoStyle)
        ws.write(13, 4, u'邮编', memberInfoStyle)
        ws.write(14, 0, u'手机', memberInfoStyle)
        ws.write(14, 4, u'家庭电话', memberInfoStyle)
        ws.write(15, 0, u'电子信箱', memberInfoStyle)
        ws.write(15, 4, u'单位电话', memberInfoStyle)
        ws.write(16, 0, u'爱好', memberInfoStyle)
        ws.write(17, 0, u'专长', memberInfoStyle)
        ws.write(1, 1, member['name'], memberInfoStyle)
        ws.write(1, 3, member['gender'], memberInfoStyle)
        ws.write_merge(1, 1, 5, 7, member['nativePlace'], memberInfoStyle)
        ws.write(2, 1, member['nation'], memberInfoStyle)
        ws.write(2, 3, member['birthPlace'], memberInfoStyle)
        ws.write_merge(2, 2, 5, 7, member['birthday'], memberInfoStyle)
        ws.write_merge(3, 3, 1, 2, member['foreignName'], memberInfoStyle)
        ws.write_merge(3, 3, 4, 7, member['usedName'], memberInfoStyle)
        ws.write_merge(4, 4, 1, 2, member['health'], memberInfoStyle)
        ws.write_merge(4, 4, 4, 7, member['marriage'], memberInfoStyle)
        ws.write_merge(5, 5, 1, 2, member['branch'], memberInfoStyle)
        ws.write_merge(5, 5, 4, 7, member['organ'], memberInfoStyle)
        ws.write_merge(6, 6, 1, 2, member['branchTime'], memberInfoStyle)
        ws.write_merge(6, 6, 4, 7, member['partyCross'], memberInfoStyle)
        ws.write_merge(7, 7, 1, 2, member['companyName'], memberInfoStyle)
        ws.write_merge(7, 7, 4, 7, member['department'], memberInfoStyle)
        ws.write_merge(8, 8, 1, 2, member['duty'], memberInfoStyle)
        ws.write_merge(8, 8, 4, 9, member['jobTitle'], memberInfoStyle)
        ws.write_merge(9, 9, 1, 2, member['academic'], memberInfoStyle)
        ws.write_merge(9, 9, 4, 5, member['jobTime'], memberInfoStyle)
        ws.write_merge(9, 9, 8, 9, member['retire'], memberInfoStyle)
        ws.write_merge(10, 10, 1, 2, member['idCard'], memberInfoStyle)
        ws.write_merge(10, 10, 4, 5, member['idType'], memberInfoStyle)
        ws.write_merge(10, 10, 8, 9, member['idNo'], memberInfoStyle)
        ws.write_merge(11, 11, 1, 3, member['homeAddress'], memberInfoStyle)
        ws.write_merge(11, 11, 5, 9, member['homePost'], memberInfoStyle)
        ws.write_merge(12, 12, 1, 3, member['companyAddress'], memberInfoStyle)
        ws.write_merge(12, 12, 5, 9, member['companyPost'], memberInfoStyle)
        ws.write_merge(13, 13, 1, 3, member['commAddress'], memberInfoStyle)
        ws.write_merge(13, 13, 5, 9, member['commPost'], memberInfoStyle)
        ws.write_merge(14, 14, 1, 3, member['mobile'], memberInfoStyle)
        ws.write_merge(14, 14, 5, 9, member['homeTel'], memberInfoStyle)
        ws.write_merge(15, 15, 1, 3, member['email'], memberInfoStyle)
        ws.write_merge(15, 15, 5, 9, member['companyTel'], memberInfoStyle)
        ws.write_merge(16, 16, 1, 9, member['hobby'], memberInfoStyle)
        ws.write_merge(17, 17, 1, 9, member['speciality'], memberInfoStyle)

        tallStyle = xlwt.easyxf('font:height 360;')
        for i in range(0, 20):
            first_row = ws.row(i)
            first_row.set_style(tallStyle)

        row = 0
        column = 0
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
        self.set_header('Content-Disposition',
                        'attachment; filename=' + urllib.parse.quote(member['name'] + '的信息.xls', "utf-8"))
        self.write(sio.getvalue())
        self.finish()
