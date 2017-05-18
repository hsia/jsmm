#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import urllib
from io import BytesIO

import tornado.web
import xlwt

from commons import couch_db, formatter_time
from lib import tornado_utils


@tornado_utils.bind_to(r'/member/exportold/([0-9a-f]+)/?')
class memberInfoExportOld(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self, member_id):

        current_row = 18

        response = couch_db.get(r'/jsmm/%(id)s' % {"id": member_id})
        member = json.loads(response.body.decode('utf-8'))

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

        wb = xlwt.Workbook()
        ws = wb.add_sheet(member['name'] + '的信息', cell_overwrite_ok=True)

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
        ws.write_merge(1, 7, 8, 9, '头像', memberInfoStyle)
        ws.write(1, 1, member.get('name', ''), memberInfoStyle)
        ws.write(1, 3, member.get('gender', ''), memberInfoStyle)
        ws.write_merge(1, 1, 5, 7, member.get('nativePlace', ''), memberInfoStyle)
        ws.write(2, 1, member.get('nation', ''), memberInfoStyle)
        ws.write(2, 3, member.get('birthPlace', ''), memberInfoStyle)
        ws.write_merge(2, 2, 5, 7, formatter_time(member.get('birthday', ''), '%Y-%m-%d'), memberInfoStyle)
        ws.write_merge(3, 3, 1, 2, member.get('foreignName', ''), memberInfoStyle)
        ws.write_merge(3, 3, 4, 7, member.get('usedName', ''), memberInfoStyle)
        ws.write_merge(4, 4, 1, 2, member.get('health', ''), memberInfoStyle)
        ws.write_merge(4, 4, 4, 7, member.get('marriage', ''), memberInfoStyle)
        ws.write_merge(5, 5, 1, 2, member.get('branch', ''), memberInfoStyle)
        ws.write_merge(5, 5, 4, 7, member.get('organ', ''), memberInfoStyle)
        ws.write_merge(6, 6, 1, 2, formatter_time(member.get('branchTime', ''), '%Y-%m-%d', '%Y.%m'), memberInfoStyle)
        ws.write_merge(6, 6, 4, 7, member.get('partyCross', ''), memberInfoStyle)
        ws.write_merge(7, 7, 1, 2, member.get('companyName', ''), memberInfoStyle)
        ws.write_merge(7, 7, 4, 7, member.get('department', ''), memberInfoStyle)
        ws.write_merge(8, 8, 1, 2, member.get('duty', ''), memberInfoStyle)
        ws.write_merge(8, 8, 4, 9, member.get('jobTitle', ''), memberInfoStyle)
        ws.write_merge(9, 9, 1, 2, member.get('academic', ''), memberInfoStyle)
        ws.write_merge(9, 9, 4, 5, formatter_time(member.get('jobTime', ''), '%Y-%m-%d', '%Y.%m'), memberInfoStyle)
        ws.write_merge(9, 9, 8, 9, member.get('retire', ''), memberInfoStyle)
        ws.write_merge(10, 10, 1, 2, member.get('idCard', ''), memberInfoStyle)
        ws.write_merge(10, 10, 4, 5, member.get('idType', ''), memberInfoStyle)
        ws.write_merge(10, 10, 8, 9, member.get('idNo', ''), memberInfoStyle)
        ws.write_merge(11, 11, 1, 3, member.get('homeAddress', ''), memberInfoStyle)
        ws.write_merge(11, 11, 5, 9, member.get('homePost', ''), memberInfoStyle)
        ws.write_merge(12, 12, 1, 3, member.get('companyAddress', ''), memberInfoStyle)
        ws.write_merge(12, 12, 5, 9, member.get('companyPost', ''), memberInfoStyle)
        ws.write_merge(13, 13, 1, 3, member.get('commAddress', ''), memberInfoStyle)
        ws.write_merge(13, 13, 5, 9, member.get('commPost', ''), memberInfoStyle)
        ws.write_merge(14, 14, 1, 3, member.get('mobile', ''), memberInfoStyle)
        ws.write_merge(14, 14, 5, 9, member.get('homeTel', ''), memberInfoStyle)
        ws.write_merge(15, 15, 1, 3, member.get('email', ''), memberInfoStyle)
        ws.write_merge(15, 15, 5, 9, member.get('companyTel', ''), memberInfoStyle)
        ws.write_merge(16, 16, 1, 9, member.get('hobby', ''), memberInfoStyle)
        ws.write_merge(17, 17, 1, 9, member.get('speciality', ''), memberInfoStyle)

        for obj in dict(member):
            for case in switch(obj):
                if case('specializedskill'):
                    if len(member.get('specializedskill', [])) > 0:
                        ws.write_merge(current_row, current_row, 0, 9, u'')
                        ws.write_merge(current_row + 1, current_row + 1, 0, 9, u'业务专长', style)
                        ws.write_merge(current_row + 2, current_row + 2, 0, 1, u'专业分类', memberInfoStyle)
                        ws.write_merge(current_row + 2, current_row + 2, 2, 4, u'专业名称', memberInfoStyle)
                        ws.write_merge(current_row + 2, current_row + 2, 5, 9, u'专业详细名称', memberInfoStyle)
                        for i in range(0, len(member.get('specializedskill', []))):
                            obj = member.get('specializedskill')[i]
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 0, 1,
                                           obj.get('specializedType', ''),
                                           memberInfoStyle)
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 2, 4,
                                           obj.get('specializedName', ''),
                                           memberInfoStyle)
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 5, 9,
                                           obj.get('specializedDetailName', ''),
                                           memberInfoStyle)
                        obj_row = 3 + len(member.get('specializedskill', []))
                        current_row += obj_row
                        break
                if case('educationDegree'):
                    if len(member['educationDegree']) > 0:
                        ws.write_merge(current_row, current_row, 0, 9, u'')
                        ws.write_merge(current_row + 1, current_row + 1, 0, 9, u'学历信息', style)
                        ws.write_merge(current_row + 2, current_row + 2, 0, 1, u'学校名称', memberInfoStyle)
                        ws.write_merge(current_row + 2, current_row + 2, 2, 3, u'起止时间', memberInfoStyle)
                        ws.write_merge(current_row + 2, current_row + 2, 4, 5, u'所学专业', memberInfoStyle)
                        ws.write(current_row + 2, 6, u'取得学历', memberInfoStyle)
                        ws.write_merge(current_row + 2, current_row + 2, 7, 8, u'所获学位', memberInfoStyle)
                        ws.write(current_row + 2, 9, u'教育类别', memberInfoStyle)
                        for i in range(0, len(member['educationDegree'])):
                            obj = member['educationDegree'][i]
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 0, 1, obj['eduSchoolName'],
                                           memberInfoStyle)
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 2, 3,
                                           formatter_time(obj['eduStartingDate'], '%Y-%m-%d', '%Y.%m') + ' - ' +
                                           formatter_time(obj['eduGraduateDate'], '%Y-%m-%d', '%Y.%m'), memberInfoStyle)
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 4, 5, obj['eduMajor'],
                                           memberInfoStyle)
                            ws.write(current_row + 3 + i, 6, obj['eduEducation'], memberInfoStyle)
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 7, 8, obj['eduDegree'],
                                           memberInfoStyle)
                            ws.write(current_row + 3 + i, 9, obj['eduEducationType'], memberInfoStyle)
                        obj_row = 3 + len(member['educationDegree'])
                        current_row += obj_row
                        break
                if case('familyRelations'):
                    if len(member['familyRelations']) > 0:
                        ws.write_merge(current_row, current_row, 0, 9, u'')
                        ws.write_merge(current_row + 1, current_row + 1, 0, 9, u'社会关系', style)
                        ws.write(current_row + 2, 0, u'姓名', memberInfoStyle)
                        ws.write(current_row + 2, 1, u'与本人关系', memberInfoStyle)
                        ws.write(current_row + 2, 2, u'性别', memberInfoStyle)
                        ws.write(current_row + 2, 3, u'出生年月', memberInfoStyle)
                        ws.write_merge(current_row + 2, current_row + 2, 4, 5, u'工作单位', memberInfoStyle)
                        ws.write(current_row + 2, 6, u'职务', memberInfoStyle)
                        ws.write(current_row + 2, 7, u'国籍', memberInfoStyle)
                        ws.write_merge(current_row + 2, current_row + 2, 8, 9, u'政治面貌', memberInfoStyle)
                        for i in range(0, len(member['familyRelations'])):
                            obj = member['familyRelations'][i]
                            ws.write(current_row + 3 + i, 0, obj['familyName'], memberInfoStyle)
                            ws.write(current_row + 3 + i, 1, obj['familyRelation'], memberInfoStyle)
                            ws.write(current_row + 3 + i, 2, obj['familyGender'], memberInfoStyle)
                            ws.write(current_row + 3 + i, 3, formatter_time(obj['familyBirthDay'], '%Y-%m-%d'),
                                     memberInfoStyle)
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 4, 5, obj['familyCompany'],
                                           memberInfoStyle)
                            ws.write(current_row + 3 + i, 6, obj['familyJob'], memberInfoStyle)
                            ws.write(current_row + 3 + i, 7, obj['familyNationality'], memberInfoStyle)
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 8, 9,
                                           obj.get('familyPolitical', ''),
                                           memberInfoStyle)
                        obj_row = 3 + len(member['familyRelations'])
                        current_row += obj_row
                        break
                if case('jobResumes'):
                    if len(member['jobResumes']) > 0:
                        ws.write_merge(current_row, current_row, 0, 9, u'')
                        ws.write_merge(current_row + 1, current_row + 1, 0, 9, u'工作履历', style)
                        ws.write_merge(current_row + 2, current_row + 2, 0, 1, u'单位名称', memberInfoStyle)
                        ws.write_merge(current_row + 2, current_row + 2, 2, 3, u'工作部门', memberInfoStyle)
                        ws.write(current_row + 2, 4, u'职务', memberInfoStyle)
                        ws.write(current_row + 2, 5, u'职称', memberInfoStyle)
                        ws.write(current_row + 2, 6, u'学术职务', memberInfoStyle)
                        ws.write_merge(current_row + 2, current_row + 2, 7, 8, u'起止时间', memberInfoStyle)
                        ws.write(current_row + 2, 9, u'证明人', memberInfoStyle)
                        for i in range(0, len(member['jobResumes'])):
                            obj = member['jobResumes'][i]
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 0, 1, obj['jobCompanyName'],
                                           memberInfoStyle)
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 2, 3, obj['jobDep'],
                                           memberInfoStyle)
                            ws.write(current_row + 3 + i, 4, obj['jobDuties'], memberInfoStyle)
                            ws.write(current_row + 3 + i, 5, obj['jobTitle'], memberInfoStyle)
                            ws.write(current_row + 3 + i, 6, obj['jobAcademic'], memberInfoStyle)
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 7, 8,
                                           formatter_time(obj.get('jobStartTime', ''), '%Y-%m-%d', '%Y.%m') + ' - ' +
                                           formatter_time(obj.get('jobEndTime', ''), '%Y-%m-%d', '%Y.%m'),
                                           memberInfoStyle)
                            ws.write(current_row + 3 + i, 9, obj['jobReterence'], memberInfoStyle)
                        obj_row = 3 + len(member['jobResumes'])
                        current_row += obj_row
                        break
                if case('award'):
                    if len(member['award']) > 0:
                        ws.write_merge(current_row, current_row, 0, 9, u'')
                        ws.write_merge(current_row + 1, current_row + 1, 0, 9, u'获奖情况', style)
                        ws.write_merge(current_row + 2, current_row + 2, 0, 2, u'获奖项目名称', memberInfoStyle)
                        ws.write(current_row + 2, 3, u'获奖时间', memberInfoStyle)
                        ws.write(current_row + 2, 4, u'获奖级别', memberInfoStyle)
                        ws.write(current_row + 2, 5, u'项目中角色', memberInfoStyle)
                        ws.write_merge(current_row + 2, current_row + 2, 6, 7, u'授予单位', memberInfoStyle)
                        ws.write_merge(current_row + 2, current_row + 2, 8, 9, u'备注', memberInfoStyle)
                        for i in range(0, len(member['award'])):
                            obj = member['award'][i]
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 0, 2, obj['awardProjectName'],
                                           memberInfoStyle)
                            ws.write(current_row + 3 + i, 3, formatter_time(obj['awardDate'], '%Y-%m-%d', '%Y.%m'),
                                     memberInfoStyle)
                            ws.write(current_row + 3 + i, 4, obj['awardNameAndLevel'], memberInfoStyle)
                            ws.write(current_row + 3 + i, 5, obj['awardRoleInProject'], memberInfoStyle)
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 6, 7, obj['awardCompany'],
                                           memberInfoStyle)
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 8, 9, obj['awardMemo'],
                                           memberInfoStyle)
                        obj_row = 3 + len(member['award'])
                        current_row += obj_row
                        break
                if case('patents'):
                    if len(member['patents']) > 0:
                        ws.write_merge(current_row, current_row, 0, 9, u'')
                        ws.write_merge(current_row + 1, current_row + 1, 0, 9, u'专利情况', style)
                        ws.write_merge(current_row + 2, current_row + 2, 0, 3, u'获专利名称', memberInfoStyle)
                        ws.write_merge(current_row + 2, current_row + 2, 4, 5, u'获专利时间', memberInfoStyle)
                        ws.write_merge(current_row + 2, current_row + 2, 6, 9, u'专利号', memberInfoStyle)
                        for i in range(0, len(member['patents'])):
                            obj = member['patents'][i]
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 0, 3, obj['patentName'],
                                           memberInfoStyle)
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 4, 5,
                                           formatter_time(obj['patentDate'], '%Y-%m-%d'),
                                           memberInfoStyle)
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 6, 9, obj['patenNo'],
                                           memberInfoStyle)
                        obj_row = 3 + len(member['patents'])
                        current_row += obj_row
                        break
                if case('paper'):
                    if len(member['paper']) > 0:
                        ws.write_merge(current_row, current_row, 0, 9, u'')
                        ws.write_merge(current_row + 1, current_row + 1, 0, 9, u'主要论文著作', style)
                        ws.write(current_row + 2, 0, u'论文/著作', memberInfoStyle)
                        ws.write_merge(current_row + 2, current_row + 2, 1, 3, u'作品名称', memberInfoStyle)
                        ws.write_merge(current_row + 2, current_row + 2, 4, 6, u'刊物/出版社', memberInfoStyle)
                        ws.write(current_row + 2, 7, u'第几作者', memberInfoStyle)
                        ws.write(current_row + 2, 8, u'发行时间', memberInfoStyle)
                        ws.write(current_row + 2, 9, u'角色说明', memberInfoStyle)
                        for i in range(0, len(member['paper'])):
                            obj = member['paper'][i]
                            ws.write(current_row + 3 + i, 0, obj['paperPublications'], memberInfoStyle)
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 1, 3, obj['paperName'],
                                           memberInfoStyle)
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 4, 6, obj['paperPress'],
                                           memberInfoStyle)
                            ws.write(current_row + 3 + i, 7, obj['paperAuthorSort'], memberInfoStyle)
                            ws.write(current_row + 3 + i, 8, formatter_time(obj['paperPressDate'], '%Y-%m-%d', '%Y.%m'),
                                     memberInfoStyle)
                            ws.write(current_row + 3 + i, 9, obj['paperRoleDetail'], memberInfoStyle)
                        obj_row = 3 + len(member['paper'])
                        current_row += obj_row
                        break
                if case('professionalSkill'):
                    if len(member['professionalSkill']) > 0:
                        ws.write_merge(current_row, current_row, 0, 9, u'')
                        ws.write_merge(current_row + 1, current_row + 1, 0, 9, u'专业技术工作', style)
                        ws.write_merge(current_row + 2, current_row + 2, 0, 3, u'项目名称', memberInfoStyle)
                        ws.write(current_row + 2, 4, u'项目类别', memberInfoStyle)
                        ws.write_merge(current_row + 2, current_row + 2, 5, 6, u'项目下达单位', memberInfoStyle)
                        ws.write(current_row + 2, 7, u'项目中所任角色', memberInfoStyle)
                        ws.write_merge(current_row + 2, current_row + 2, 8, 9, u'起止时间', memberInfoStyle)
                        for i in range(0, len(member['professionalSkill'])):
                            obj = member['professionalSkill'][i]
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 0, 3, obj['proProjectName'],
                                           memberInfoStyle)
                            ws.write(current_row + 3 + i, 4, obj['proProjectType'], memberInfoStyle)
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 5, 6, obj['proProjectCompany'],
                                           memberInfoStyle)
                            ws.write(current_row + 3 + i, 7, obj['proRolesInProject'], memberInfoStyle)
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 8, 9,
                                           formatter_time(obj['proStartDate'], '%Y-%m-%d', '%Y.%m') + ' - ' +
                                           formatter_time(obj['porEndDate'], '%Y-%m-%d', '%Y.%m'), memberInfoStyle)
                        obj_row = 3 + len(member['professionalSkill'])
                        current_row += obj_row
                        break
                if case('achievements'):
                    if len(member['achievements']) > 0:
                        ws.write_merge(current_row, current_row, 0, 9, u'')
                        ws.write_merge(current_row + 1, current_row + 1, 0, 9, u'专业技术成果', style)
                        ws.write_merge(current_row + 2, current_row + 2, 0, 2, u'成果名称', memberInfoStyle)
                        ws.write_merge(current_row + 2, current_row + 2, 3, 5, u'成果水平', memberInfoStyle)
                        ws.write_merge(current_row + 2, current_row + 2, 6, 7, u'鉴定单位', memberInfoStyle)
                        ws.write_merge(current_row + 2, current_row + 2, 8, 9, u'备注', memberInfoStyle)
                        for i in range(0, len(member['achievements'])):
                            obj = member['achievements'][i]
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 0, 2, obj['achievementsName'],
                                           memberInfoStyle)
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 3, 5, obj['achievementsLevel'],
                                           memberInfoStyle)
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 6, 7, obj['identificationUnit'],
                                           memberInfoStyle)
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 8, 9, obj['achievementsRemark'],
                                           memberInfoStyle)
                        obj_row = 3 + len(member['achievements'])
                        current_row += obj_row
                        break
                if case('agencybroker'):
                    if len(member['agencybroker']) > 0:
                        ws.write_merge(current_row, current_row, 0, 9, u'')
                        ws.write_merge(current_row + 1, current_row + 1, 0, 9, u'入社介绍人', style)
                        ws.write_merge(current_row + 2, current_row + 2, 0, 1, u'姓名', memberInfoStyle)
                        ws.write_merge(current_row + 2, current_row + 2, 2, 4, u'单位', memberInfoStyle)
                        ws.write_merge(current_row + 2, current_row + 2, 5, 6, u'职务', memberInfoStyle)
                        ws.write_merge(current_row + 2, current_row + 2, 7, 9, u'与本人关系', memberInfoStyle)
                        for i in range(0, len(member['agencybroker'])):
                            obj = member['agencybroker'][i]
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 0, 1, obj['agencyName'],
                                           memberInfoStyle)
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 2, 4, obj['agencyCompany'],
                                           memberInfoStyle)
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 5, 6, obj['agencyJob'],
                                           memberInfoStyle)
                            ws.write_merge(current_row + 3 + i, current_row + 3 + i, 7, 9, obj['agencyRelationShip'],
                                           memberInfoStyle)
                        obj_row = 3 + len(member['agencybroker'])
                        current_row += obj_row
                        break
                if self.request.arguments:
                    current_row = customizeObj(obj, current_row, ws, style, memberInfoStyle, member)

        tall_style = xlwt.easyxf('font:height 360;')
        for i in range(0, current_row):
            first_row = ws.row(i)
            first_row.set_style(tall_style)

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


class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        yield self.match
        raise StopIteration

    def match(self, *args):
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False


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

# @tornado_utils.bind_to(r'/member/information/(.+)')
# class MembersExport(tornado.web.RequestHandler):
#     @tornado.web.addslash
#     def get(self, search_obj):
#         keys = ['name', 'gender', 'sector', 'lost', 'stratum', 'jobLevel', 'titleLevel', 'highestEducation']
#         column_name = ["name", "gender", "highestEducation", "jobTitle", "duty", "mobile",
#                        "email", "companyName", "companyTel", "commAddress", "commPost"]
#         titles = {u'姓名': 10, u'性别': 6, u'最高学历': 10, u'职称': 12, u'职务': 12, u'移动电话': 13, u'邮箱': 25, u'单位名称': 26,
#                   u'单位电话': 15, u'单位地址': 40, u'邮编': 10}
#         selector = {
#             "selector": {},
#             "fields": column_name
#         }
#         selector_content = selector["selector"]
#         search = json.loads(search_obj.replace('/', ''))
#
#         for key in keys:
#             if key in search:
#                 if search[key] != '':
#                     selector_content[key] = {'$regex': search[key]}
#
#         if 'retireTime' in search:
#             if search['retireTime'] != '':
#                 selector_content['retireTime'] = {"$lt": search["retireTime"]}
#
#         if 'branch' in search:
#             if search['branch'] != '' and search['branch'] != u'北京市' and search['branch'] != u'朝阳区':
#                 selector_content['branch'] = {"$eq": search["branch"]}
#
#         if 'socialPositionName' in search:
#             if search['socialPositionName'] != '':
#                 selector_content['social'] = {
#                     "$elemMatch": {"socialPositionName": {"$regex": search['socialPositionName']}}}
#
#         if 'socialPositionLevel' in search:
#             if search['socialPositionLevel'] != '':
#                 selector_content['social'] = {
#                     "$elemMatch": {"socialPositionLevel": {"$regex": search['socialPositionLevel']}}}
#
#         if 'formeOrganizationJob' in search:
#             if search['formeOrganizationJob'] != '':
#                 selector_content['formercluboffice'] = {
#                     "$elemMatch": {"formeOrganizationJob": {"$regex": search['formeOrganizationJob']}}}
#
#         if 'formeOrganizationLevel' in search:
#             if search['formeOrganizationLevel'] != '':
#                 selector_content['formercluboffice'] = {
#                     "$elemMatch": {"formeOrganizationLevel": {"$regex": search['formeOrganizationLevel']}}}
#
#         if 'startAge' in search and 'endAge' in search:
#             if search['startAge'] != '' and search['endAge']:
#                 selector_content['birthday'] = {"$gte": search['endAge'], "$lte": search['startAge']}
#
#         selector_content['type'] = {"$eq": "member"}
#
#         response = couch_db.post(r'/jsmm/_find/', selector)
#         members_simple_info = json.loads(response.body.decode('utf-8'))["docs"]
#
#         style_heading = xlwt.easyxf("""
#                 font:
#                     name 微软雅黑,
#                     colour_index black,
#                     bold on,
#                     height 200;
#                 align:
#                     wrap off,
#                     vert center,
#                     horiz centre;
#                 pattern:
#                     pattern solid,
#                     fore-colour 22;
#                 borders:
#                     left THIN,
#                     right THIN,
#                     top THIN,
#                     bottom THIN;
#                 """)
#         style_data = xlwt.easyxf("""
#                         font:
#                             name 微软雅黑,
#                             colour_index black,
#                             bold off,
#                             height 180;
#                         align:
#                             wrap off,
#                             vert center,
#                             horiz left;
#                         pattern:
#                             pattern solid,
#                             fore-colour 1;
#                         borders:
#                             left thin,
#                             right thin,
#                             top thin,
#                             bottom thin;
#                         """)
#
#         workbook = xlwt.Workbook()
#         worksheet = workbook.add_sheet('社员信息简表')
#
#         column = 0
#         row = 0
#         for title in titles:
#             worksheet.write(row, column, title, style_heading)
#             worksheet.col(column).width = titles[title] * 256
#             column += 1
#
#         if len(members_simple_info) > 0:
#             row = 1
#             for member in members_simple_info:
#                 column = 0
#                 for key in column_name:
#                     worksheet.write(row, column, '', style_data) if key not in member else worksheet.write(row, column,
#                                                                                                            member[key],
#                                                                                                            style_data)
#                     column += 1
#
#                 row += 1
#         else:
#             pass
#
#         sio = BytesIO()
#         workbook.save(sio)
#
#         agent = self.request.headers.get('User-Agent')
#         if 'Firefox' in agent:
#             if self.request.arguments:
#                 download_file_name = "attachment;filename*=utf-8'zh_cn'" + urllib.parse.quote(
#                     '社员信息汇总表.xls',
#                     "utf-8")
#             else:
#                 download_file_name = "attachment;filename*=utf-8'zh_cn'" + urllib.parse.quote(
#                     '社员信息汇总表.xls',
#                     "utf-8")
#         else:
#             if self.request.arguments:
#                 download_file_name = 'attachment; filename=' + urllib.parse.quote(
#                     '社员信息汇总表.xls', "utf-8")
#             else:
#                 download_file_name = 'attachment; filename=' + urllib.parse.quote(
#                     '社员信息汇总表.xls', "utf-8")
#         self.set_header('Content-Type', 'application/vnd.ms-excel')
#         self.set_header('Content-Disposition', download_file_name)
#         self.write(sio.getvalue())
#         self.finish()
