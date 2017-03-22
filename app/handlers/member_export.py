#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xlwt
import tornado.web
import tornado_utils
import urllib
from io import BytesIO

@tornado_utils.bind_to(r'/member/export/')
class memberExport(tornado.web.RequestHandler):

    @tornado.web.addslash
    def get(self):

        # style0 = xlwt.easyxf('font: name Times New Roman', 'pattern_fore_colour Blue', 'font: bold 1')

        wb = xlwt.Workbook()
        ws = wb.add_sheet('A Test Sheet')

        ws.write(0, 0, 'dfa')
        sio = BytesIO()
        wb.save(sio)
        self.set_header('Content-Type', 'application/vnd.ms-excel')
        self.set_header('Content-Disposition', 'attachment; filename=student_info.xls')
        self.write(sio.getvalue())
