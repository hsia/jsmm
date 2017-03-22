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

        style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')

        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 22
        style = xlwt.XFStyle()
        style.pattern = pattern

        wb = xlwt.Workbook()
        ws = wb.add_sheet('A Test Sheet', cell_overwrite_ok=True)

        # ws.write(0, 0, 'dfa', style)
        ws.write_merge(0, 0, 0, 3, 'First Merge')
        sio = BytesIO()
        wb.save(sio)
        self.set_header('Content-Type', 'application/vnd.ms-excel')
        self.set_header('Content-Disposition', 'attachment; filename=student_info.xls')
        self.write(sio.getvalue())
