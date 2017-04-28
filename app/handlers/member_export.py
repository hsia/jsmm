#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import urllib
from io import BytesIO
import time
import tornado.web
import tornado_utils
import xlwt

from commons import couch_db, formatter_time


@tornado_utils.bind_to(r'/member/export/([0-9a-f]+)/?')
class memberInfoExport(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self, member_id):

        response = couch_db.get(r'/jsmm/%(id)s' % {"id": member_id})
        member = json.loads(response.body.decode('utf-8'))

        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 22
        style = xlwt.XFStyle()
        style.borders.THIN
        style.pattern = pattern
        style.font.height = 220
        style.font.name = '宋体'

        borders = xlwt.Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        borders.bottom_colour = 0x3A

        memberInfoStyle = xlwt.XFStyle()
        memberInfoStyle.borders = borders
        memberInfoStyle.font.name = '宋体'
        memberInfoStyle.font.height = 220

        wb = xlwt.Workbook()
        basic_head_width = {u'title': 10, u'content': 6, u'说明': 10, u'标准代码': 12}
        # 基本信息
        basic_info_properties = {"name": u"姓名", "foreignName": u"外文姓名", "usedName": u"曾用名", "gender": u"性别",
                                 "birthday": "出生日期", "nativePlace": u"籍贯", "birthPlace": u"出生地", "nation": u"民族",
                                 "health": u"健康状态", "marriage": u"婚姻状态", "idCard": u"公民身份证号码",
                                 "idType": u"有效证件类别", "idNo": u"证件号码", "branch": u"所属支社",
                                 "organ": u"所属基层组织名称", "branchTime": u"入社时间", "partyCross": u"党派交叉",
                                 "companyName": u"单位名称", "jobTime": u"参加工作时间", "department": u"工作部门",
                                 "retire": u"是否办理退休手续", "duty": u"职务", "jobTitle": u"职称", "academic": u"学术职务",
                                 "homeAddress": u"家庭地址", "homePost": u"家庭地址邮编", "homeTel": u"家庭电话",
                                 "companyAddress": u"单位地址", "companyPost": u"单位地址邮编", "commAddress": u"通信地址",
                                 "commPost": u"通信地址邮编", "mobile": u"移动电话", "email": u"电子信箱",
                                 "companyTel": u"单位电话", "hobby": u"爱好", "speciality": u"专长"}
        # 学历信息
        educationDegree_header = {"eduSchoolName": u"学校（单位）名称 A0435",
                                  "eduStartingDate": u"入学日期 A0415",
                                  "eduGraduateDate": u"毕业日期 A0430",
                                  "eduMajor": u"所学专业 A0410",
                                  "eduEducation": u"学历 A0405",
                                  "eduDegree": u"学位 A0440",
                                  "eduEducationType": u"教育类别 A0449"}
        # 工作履历
        jobResumes_header = {"jobCompanyName": u"单位名称 A1915",
                             "jobDep": u"工作部门",
                             "jobDuties": u"职务 A1920",
                             "jobTitle": u"职称",
                             "jobAcademic": u"学术职务",
                             "jobStartTime": u"开始时间 A1905",
                             "jobEndTime": u"结束时间 A1910",
                             "jobReterence": u"证明人 A1925"}
        # 专业技术工作
        professionalSkill_header = {"proProjectName": u"项目名称 A4305",
                                    "proProjectType": u"项目类别 A4315",
                                    "proProjectCompany": u"项目下达单位 A4320",
                                    "proRolesInProject": u"项目中所任角色 A4340",
                                    "proStartDate": u"开始时间 A4330",
                                    "porEndDate": u"结束时间 A4335"}
        # 家庭社会关系
        familyRelations_header = {"familyName": u"姓名 A7905",
                                  "familyRelation": u"与本人的关系 A7910",
                                  "familyGender": u"性别",
                                  "familyBirthDay": u"出生年月 A7915",
                                  "familyCompany": u"工作单位 A7920",
                                  "familyJob": u"职务",
                                  "familyNationality": u"国籍 A7907",
                                  "familyPolitical": u"政治面貌 A7925"}
        # 论文著作
        paper_header = {"paperPublications": u"论文/著作 A4505",
                        "paperName": u"作品名称 A4515",
                        "paperPress": u"刊物/出版社 A4525",
                        "paperAuthorSort": u"第几作者",
                        "paperPressDate": u"发行时间 A4510",
                        "paperRoleDetail": u"角色说明 A4530"}
        # 专业技术成果
        achievements_header = {"achievementsName": u"成果名称 A4605",
                               "achievementsLevel": u"成果水平 A4615",
                               "identificationUnit": u"鉴定单位 A4620",
                               "achievementsRemark": u"备注"}
        # A49.专业技术工作获奖
        award_header = {"awardProjectName": u"获奖项目名称 A4910",
                        "awardDate": u"获奖日期 A4905",
                        "awardNameAndLevel": u"获奖名称及级别 A4925",
                        "awardRoleInProject": u"项目中角色 A4920",
                        "awardCompany": u"授予单位 A4925",
                        "awardMemo": u"备注"}

        # A52.专利情况
        patents_header = {"patentName": u"获专利名称 A5210",
                          "patentDate": u"获专利时间 A5205",
                          "patenNo": u"专利号 A5215"}
        # A70.专家情况
        professor_header = {"professorName": u"专家名称 A7005",
                            "approvalDate": u"批准时间 A7020",
                            "approvalCompanyLevel": u"批准单位级别A7015",
                            "approvalCompanyName": u"批准单位名称 A7010",
                            "govSubsidiesType": u"政府津贴类别",
                            "subsidiesDate": u"享受津贴时间"}
        # 业务专长
        specializedskill_header = {"specializedType": u"专业分类",
                                   "specializedName": u"专业名称",
                                   "specializedDetailName": u"专业详细名称"}
        # 历任社内职务
        formerClubOffice_header = {"formerOrganizationCategory": u"社内组织类别",
                                   "formerOrganizationName": u"社内组织名称",
                                   "formerOrganizationLevel": u"社会组织级别",
                                   "formerOrganizationJob": u"社内职务名称",
                                   "formerTheTime": u"届次",
                                   "formerStartTime": u"开始时间",
                                   "formerEndTime": "结束时间"}
        # 政府和主要社会职务
        social_headers = {"socialOrgType": u"社会组织类别",
                          "socialOrgName": u"社会组织名称",
                          "socialPositionLevel": u"社会职务级别",
                          "socialPositionName": u"社会职务名称",
                          "socialPeriod": u"届次",
                          "socialBeginDate": u"开始时间",
                          "socialEndDate": u"结束时间"}
        # 其它社会职务
        socialduties_header = {"socialOrganizationCategory": u"社会组织类别",
                               "socialOrganizationLevel": u"社会组织名称",
                               "socialPositionLevel": u"社会职务级别",
                               "socialOrganizationJob": u"社会职务名称",
                               "socialTheTime": u"届次",
                               "socialStartTime": u"开始时间",
                               "socialEndTime": u"结束时间"}
        # 入社介绍人
        agencybroker_header = {"agencyName": u"姓名",
                               "agencyCompany": u"单位",
                               "agencyJob": u"职务",
                               "agencyRelationShip": u"与本人关系"}

        sheet_names_info = {"educationDegree": [u"A04.学历与学位", u"学历及学位 A04", educationDegree_header],
                            "jobResumes": [u"A19.工作履历", u"工作履历 A19", jobResumes_header],
                            "professionalSkill": [u"A43.专业技术工作", u"专业技术工作:", professionalSkill_header],
                            "familyRelations": [u"A79.家庭社会关系", u"家庭成员及社会关系（包括海外社会关系） A79", familyRelations_header],
                            "paper": [u"A45.主要论文著作", U"主要论文及著作情况 A45", paper_header],
                            "achievements": [u"A46.专业技术成果", u"专业技术成果，A46", achievements_header],
                            "award": [u"A49.专业技术工作获奖", u"专业技术工作获奖， A49", award_header],
                            "patents": [u"A52.专利情况", u"专利情况, A52", patents_header],
                            "professor": [u"A70.专家情况", u"专家情况：A70", professor_header],
                            "specializedskill": [u"业务专长", u"业务专长：", specializedskill_header],
                            "formerClubOffice": [u"历任社内职务", u"历任社内职务", formerClubOffice_header],
                            "social": [u"政府和主要社会职务", u"政府和主要社会职务（包括各级政府、人大、政协、特邀职务、青联、侨联、妇联）", social_headers],
                            "socialduties": [u"其它社会职务", u"其它社会职务（包括各类社会团体和学术团体）", socialduties_header],
                            "agencybroker": [u"入社介绍人", u"入社介绍人：", agencybroker_header]}

        self.basic_info_sheet(wb, basic_info_properties, member, memberInfoStyle, memberInfoStyle)
        self.sheet_names_info_sheet(wb, sheet_names_info, member, memberInfoStyle, memberInfoStyle)

        sio = BytesIO()
        wb.save(sio)
        # 判断浏览器类型

        agent = self.request.headers.get('User-Agent')
        if 'Firefox' in agent:
            if self.request.arguments:
                download_file_name = "attachment;filename*=utf-8'zh_cn'" + urllib.parse.quote(
                    member.get('branch') + '-' + member.get('name') + '的信息-自定义.xls',
                    "utf-8")
            else:
                download_file_name = "attachment;filename*=utf-8'zh_cn'" + urllib.parse.quote(
                    member.get('branch') + '-' + member.get('name') + '的信息.xls',
                    "utf-8")
        else:
            if self.request.arguments:
                download_file_name = 'attachment; filename=' + urllib.parse.quote(
                    member.get('branch') + '-' + member.get('name') + '的信息-自定义.xls', "utf-8")
            else:
                download_file_name = 'attachment; filename=' + urllib.parse.quote(
                    member.get('branch') + '-' + member.get('name') + '的信息.xls', "utf-8")

        self.set_header('Content-Type', 'application/vnd.ms-excel')
        self.set_header('Content-Disposition', download_file_name)
        self.write(sio.getvalue())
        self.finish()

    def basic_info_sheet(self, work_book, basic_info_properties, member_info, style_header, style_body):
        """
        获得基本信息
        :param work_book 写入Excel:
        :param basic_info_properties 社员信息表属性和存储的属性对应关系 “name”:u"姓名":
        :param member_info 社员信息表:
        :param style_header 标题样式:
        :param style_body 内容样式:
        :return:
        """
        # 新建基本信息sheet，名称： u'A01.基本信息页'
        worksheet = work_book.add_sheet(u'A01.基本信息页', cell_overwrite_ok=True)
        # 标题
        worksheet.col(0).width = 5 * 256
        worksheet.col(1).width = 20 * 256
        worksheet.col(2).width = 30 * 256
        worksheet.col(3).width = 30 * 256
        worksheet.col(4).width = 10 * 256
        # 设置行高
        tall_style = xlwt.easyxf('font:height 360;')
        worksheet.row(1).set_style(tall_style)

        worksheet.write_merge(1, 1, 1, 2, u'个人信息-基本情况 A01', style_header)
        worksheet.write(1, 3, u'说明', style_header)
        worksheet.write(1, 4, u'标准代码', style_header)
        # 内容
        row_number = 2
        for key in basic_info_properties:
            worksheet.write(row_number, 1, basic_info_properties.get(key), style_body)
            worksheet.write(row_number, 2, member_info.get(key, ''), style_body)
            worksheet.write(row_number, 3, '', style_body)
            worksheet.write(row_number, 4, '', style_body)
            row_number += 1

    def sheet_names_info_sheet(self, work_book, sheet_names_infos, member_info, style_header, style_body):
        # "educationDegree": [u"A04.学历与学位", u"学历及学位 A04", {}],
        for sheet_key in sheet_names_infos:
            # 获得数据库中sheet_key中的数据
            key_info_in_db = member_info.get(sheet_key, [])
            if key_info_in_db:
                # 获得sheet名称，标题和列名
                sheet_name = sheet_names_infos.get(sheet_key)[0]
                sheet_title = sheet_names_infos.get(sheet_key)[1]
                sheet_column = sheet_names_infos.get(sheet_key)[2]
                # 新建sheet名称为XXX
                worksheet = work_book.add_sheet(sheet_name, cell_overwrite_ok=True)
                # 写入sheet标题
                worksheet.write_merge(0, 0, 1, len(sheet_column), sheet_title, style_body)
                # 写入sheet列名
                header_column_number = 1
                worksheet.col(0).width = 5 * 256
                for header_key in sheet_column:
                    # 列名
                    column_name = sheet_column.get(header_key)
                    worksheet.col(header_column_number).width = 20 * 256
                    worksheet.write(1, header_column_number, column_name, style_header)
                    header_column_number += 1

                # 写入sheet内容
                key_column_number = 2
                for info_key in key_info_in_db:
                    row_number = 1
                    for key_row_value in sheet_column:
                        value = info_key.get(key_row_value, '')
                        worksheet.write(key_column_number, row_number, value, style_body)
                        row_number += 1
                    key_column_number += 1

    def customizeObj(obj, current_row, ws, style, memberInfoStyle, member):
        if len(obj) > 6:
            if obj[0:7] == 'custab_':
                selector = {
                    "selector": {
                        "type": {
                            "$eq": "tab"
                        },
                        "tab_id": {
                            "$eq": obj
                        }
                    }
                }
                response = couch_db.post(r'/jsmm/_find/', selector)
                tab = json.loads(response.body.decode('utf-8'))
                tabObj = tab['docs'][0]
                ws.write_merge(current_row, current_row, 0, 9, u'')
                ws.write_merge(current_row + 1, current_row + 1, 0, 9, tabObj['gridTitle'], style)
                columns = tabObj['columns']
                for y in range(0, len(columns)):
                    ws.write(current_row + 2, y, columns[y]['title'], memberInfoStyle)

                for i in range(0, len(member[obj])):
                    memberObj = member[obj][i]
                    x = 0
                    for z in columns:
                        print(z.get('title') + ":" + memberObj.get(z.get('field'), ''))
                        ws.write(current_row + 3 + i, x, memberObj.get(z.get('field'), ''), memberInfoStyle)
                        x += 1

                obj_row = 3 + len(member[obj])
                current_row += obj_row
        return current_row


@tornado_utils.bind_to(r'/member/information/(.+)')
class MembersExport(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self, search_obj):
        keys = ['name', 'gender', 'sector', 'lost', 'stratum', 'jobLevel', 'titleLevel', 'highestEducation']
        column_name = ["name", "gender", "highestEducation", "jobTitle", "duty", "mobile",
                       "email", "companyName", "companyTel", "commAddress", "commPost"]
        titles = {u'姓名': 10, u'性别': 6, u'最高学历': 10, u'职称': 12, u'职务': 12, u'移动电话': 13, u'邮箱': 25, u'单位名称': 26,
                  u'单位电话': 15, u'单位地址': 40, u'邮编': 10}
        selector = {
            "selector": {},
            "fields": column_name
        }
        selector_content = selector["selector"]
        search = json.loads(search_obj.replace('/', ''))

        for key in keys:
            if key in search:
                if search[key] != '':
                    selector_content[key] = {'$regex': search[key]}

        if 'retireTime' in search:
            if search['retireTime'] != '':
                selector_content['retireTime'] = {"$lt": search["retireTime"]}

        if 'branch' in search:
            if search['branch'] != '' and search['branch'] != u'北京市' and search['branch'] != u'朝阳区':
                selector_content['branch'] = {"$eq": search["branch"]}

        if 'socialPositionName' in search:
            if search['socialPositionName'] != '':
                selector_content['social'] = {
                    "$elemMatch": {"socialPositionName": {"$regex": search['socialPositionName']}}}

        if 'socialPositionLevel' in search:
            if search['socialPositionLevel'] != '':
                selector_content['social'] = {
                    "$elemMatch": {"socialPositionLevel": {"$regex": search['socialPositionLevel']}}}

        if 'formeOrganizationJob' in search:
            if search['formeOrganizationJob'] != '':
                selector_content['formercluboffice'] = {
                    "$elemMatch": {"formeOrganizationJob": {"$regex": search['formeOrganizationJob']}}}

        if 'formeOrganizationLevel' in search:
            if search['formeOrganizationLevel'] != '':
                selector_content['formercluboffice'] = {
                    "$elemMatch": {"formeOrganizationLevel": {"$regex": search['formeOrganizationLevel']}}}

        if 'startAge' in search and 'endAge' in search:
            if search['startAge'] != '' and search['endAge']:
                selector_content['birthday'] = {"$gte": search['endAge'], "$lte": search['startAge']}

        selector_content['type'] = {"$eq": "member"}

        response = couch_db.post(r'/jsmm/_find/', selector)
        members_simple_info = json.loads(response.body.decode('utf-8'))["docs"]

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

        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('社员信息简表')

        column = 0
        row = 0
        for title in titles:
            worksheet.write(row, column, title, style_heading)
            worksheet.col(column).width = titles[title] * 256
            column += 1

        if len(members_simple_info) > 0:
            row = 1
            for member in members_simple_info:
                column = 0
                for key in column_name:
                    worksheet.write(row, column, '', style_data) if key not in member else worksheet.write(row, column,
                                                                                                           member[key],
                                                                                                           style_data)
                    column += 1

                row += 1
        else:
            pass

        sio = BytesIO()
        workbook.save(sio)

        agent = self.request.headers.get('User-Agent')
        if 'Firefox' in agent:
            if self.request.arguments:
                download_file_name = "attachment;filename*=utf-8'zh_cn'" + urllib.parse.quote(
                    '社员信息汇总表.xls',
                    "utf-8")
            else:
                download_file_name = "attachment;filename*=utf-8'zh_cn'" + urllib.parse.quote(
                    '社员信息汇总表.xls',
                    "utf-8")
        else:
            if self.request.arguments:
                download_file_name = 'attachment; filename=' + urllib.parse.quote(
                    '社员信息汇总表.xls', "utf-8")
            else:
                download_file_name = 'attachment; filename=' + urllib.parse.quote(
                    '社员信息汇总表.xls', "utf-8")
        self.set_header('Content-Type', 'application/vnd.ms-excel')
        self.set_header('Content-Disposition', download_file_name)
        self.write(sio.getvalue())
        self.finish()
