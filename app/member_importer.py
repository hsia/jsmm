#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright lixia@ccrise.com
'''
import re
import traceback
import uuid
from enum import Enum, unique

from xlrd import open_workbook
from commons import couch_db, get_retire_time
import json


def make_uuid():
    '''
    生成随机的UUID，并返回16进制字符串
    '''
    return uuid.uuid4().hex


def format_date(date_str):
    """
    格式化从社员信息文件中导入的日期数据：
    YYYY.MM.DD -> YYYY-MM-DD
    YYYY.MM -> YYYY-MM-01
    """
    date_str = date_str.rstrip('.')  # 去除尾部的'.', 如'2010.01.'
    if date_str == u'至今' or date_str == '':  # '至今'
        return ''
    splited = date_str.split('.')  # 'YYYY', 'YYYY.MM'或'YYYY.MM.DD'
    if len(splited) == 1:  # ['YYYY']
        splited += ['01', '01']  # ['YYYY', '01', '01']
    elif len(splited) == 2:  # ['YYYY', 'MM']
        splited.append('01')  # ['YYYY', 'MM', '01']
    return '-'.join(splited)  # 'YYYY-MM-DD'


@unique
class ErrorType(Enum):
    """使用枚举定义错误类型
    """
    SHEETERROR = u'Excel中sheet名称或者数量和标准格式不一致'
    NAMEERROR = u'基本信息表中姓名不能为空'
    NAMEALLDIGITERROR = u'基本信息表中姓名不能全部是数字'
    BIRTHDAYERROR = u'基本信息表中出生日期不能为空'
    BRANCHERROR = u'基本信息表中所属支社不能为空'
    FILETYPEERROR = u'文件类型错误,只能导入.xls.xlsx'
    FILEREPEATERROR = u'社员信息重复(姓名+出生日期)'
    DATAFORMATEERROR = u'日期格式错误(正确格式ex:1980.01.01)'
    OTHERERROR = u'其他错误'


def import_info(file_info):
    """返回错误的格式
        成功：{"success":True}
        错误：{"success":False, "fileName":file_name,"errorContent":ErrorType.errorType.value}

    """
    try:
        # 文件格式错误
        if 'excel' not in file_info['content_type'] and 'sheet' not in file_info['content_type']:
            result = {"success": False, "fileName": file_info["filename"],
                      "errorContent": ErrorType.FILETYPEERROR.value}
        else:
            member_info_importer = MemberInfoImporter(file_info)
            # sheet数量、名称检查
            check_sheet_result = member_info_importer.checkSheet(file_info["filename"]);
            if check_sheet_result:
                result = member_info_importer.checkSheet(file_info["filename"])
            else:
                member_info_importer.get_basic_info()
                if not member_info_importer.member.get('name', ''):
                    # 基础信息表中姓名为空
                    result = {"success": False, "fileName": file_info["filename"],
                              "errorContent": ErrorType.NAMEERROR.value}
                elif type(member_info_importer.member.get('name')) == float:
                    # 基础信息表中姓名全部位数字
                    result = {"success": False, "fileName": file_info["filename"],
                              "errorContent": ErrorType.NAMEALLDIGITERROR.value}
                elif not member_info_importer.member.get('birthday', ''):
                    # 基础信息表中出生日期为空
                    result = {"success": False, "fileName": file_info["filename"],
                              "errorContent": ErrorType.BIRTHDAYERROR.value}
                elif not member_info_importer.member.get('branch', ''):
                    # 基础信息表中所属支社为空
                    result = {"success": False, "fileName": file_info["filename"],
                              "errorContent": ErrorType.BRANCHERROR.value}
                else:
                    member_info_importer.main_function()
                    result = member_info_importer.save_member(file_info["filename"])

    except Exception as e:
        print(Exception, ":", e)
        result = {"success": False, "fileName": file_info["filename"], "errorContent": ErrorType.OTHERERROR.value}
    finally:
        return result


class MemberInfoImporter:
    """
    导入社员信息。
    """

    def __init__(self, file_info):
        """
        打开一个包含社员基本信息的Excel文件。
        :param file_info['path']:
        """
        self._book = open_workbook(file_info['path'])

        self._member = {
            'type': 'member',
            '_id': make_uuid(),
            'educationDegree': [],  # 学历信息       1
            'jobResumes': [],  # 工作履历       1
            'professionalSkill': [],  # 专业技术工作   1
            'familyRelations': [],  # 社会关系       1
            'paper': [],  # 主要论文著作   1
            'achievements': [],  # 专业技术成果   1
            'award': [],  # 获奖情况       1
            'patents': [],  # 专利情况       1
            'professor': [],  # 专家情况       0
            'specializedskill': [],  # 业务专长       1
            'formerClubOffice': [],  # 社内职务       0
            'social': [],  # 社会职务       0
            'socialduties': [],  # 其它职务       0
            'agencybroker': []  # 入社介绍人     1
        }
        self._tabs_name = {
            u"学历信息": self.member_edu_degree,  # 学历信息
            u"工作履历": self.member_job_resumes,  # 工作履历
            u"专业技术工作": self.member_professional,  # 专业技术工作
            u"社会关系": self.member_family_relation,  # 社会关系
            u"主要论文著作": self.member_paper,  # 主要论文著作
            u"专业技术成果": self.member_achievements,  # 专业技术成果
            u"获奖情况": self.member_award,  # 获奖情况
            u"专利情况": self.member_patents,  # 专利情况
            u"专家情况": self.member_professor,  # 专家情况
            u"业务专长": self.member_specialized_skill,  # 业务专长
            u"社内职务": self.member_former_club_office,  # 社内职务
            u"社会职务": self.member_social,  # 社会职务
            u"其它职务": self.member_social_duties,  # 其它职务
            u"入社介绍人": self.member_agency_broker  # 入社介绍人
        }
        # print(r'正在处理%(path)s' % {'path': path})

    def checkSheet(self, file_name):
        """判断sheet数量和名称是否一致
                """
        # 表中格式的sheet名称列表
        sheet_names = [u'字典表数据', u'组织机构', u'填写说明', u'A01.基本信息页',
                       u'A04.学历与学位', u'A19.工作履历', u'A43.专业技术工作', u'A79.家庭社会关系',
                       u'A45.主要论文著作', u'A46.专业技术成果', u'A49.专业技术工作获奖', u'A52.专利情况',
                       u'A70.专家情况', u'业务专长', u'历任社内职务', u'政府和主要社会职务',
                       u'其它社会职务', u'入社介绍人']
        sheets_names_excel = self._book.sheet_names()

        if set(sheet_names).difference(set(sheets_names_excel)):
            return {"success": False, "fileName": file_name, "errorContent": ErrorType.SHEETERROR.value}

    def get_basic_info(self):
        """
        获取"基本信息页"
        :return:
        """
        basic_info_sheet = self._book.sheet_by_name(u'A01.基本信息页')
        basic_info_mapper = {
            (2, 2): "name",  # 姓名
            (3, 2): "foreignName",  # 外文姓名
            (4, 2): "usedName",  # 曾用名
            (5, 2): "gender",  # 性别
            (6, 2): "birthday",  # 出生日期
            (7, 2): "nativePlace",  # 籍贯
            (8, 2): "birthPlace",  # 出生地
            (9, 2): "nation",  # 民族
            (10, 2): "health",  # 健康状态
            (11, 2): "marriage",  # 婚姻状态
            (12, 2): "idCard",  # 公民身份证号码
            (13, 2): "idType",  # 有效证件类别
            (14, 2): "idNo",  # 证件号码
            (15, 2): "branch",  # 所属支社
            (16, 2): "organ",  # 所属基层组织名称
            (17, 2): "branchTime",  # 入社时间
            (18, 2): "partyCross",  # 党派交叉
            (19, 2): "companyName",  # 单位名称
            (20, 2): "jobTime",  # 参加工作时间
            (21, 2): "department",  # 工作部门
            (22, 2): "retire",  # 是否办理退休手续
            (23, 2): "duty",  # 职务
            (24, 2): "jobTitle",  # 职称
            (25, 2): "academic",  # 学术职务
            (26, 2): "homeAddress",  # 家庭地址
            (27, 2): "homePost",  # 家庭地址邮编
            (28, 2): "homeTel",  # 家庭电话
            (29, 2): "companyAddress",  # 单位地址
            (30, 2): "companyPost",  # 单位地址邮编
            (31, 2): "commAddress",  # 通信地址
            (32, 2): "commPost",  # 通信地址邮编
            (33, 2): "mobile",  # 移动电话
            (34, 2): "email",  # 电子信箱
            (35, 2): "companyTel",  # 单位电话
            (36, 2): "hobby",  # 爱好
            (37, 2): "speciality"  # 专长
        }

        for key in basic_info_mapper.keys():
            self._member[basic_info_mapper[key]] = basic_info_sheet.cell_value(key[0], key[1])
        self._member['branchTime'] = format_date(str(self._member['branchTime']))
        self._member['birthday'] = format_date(str(self._member['birthday']))
        self._member['jobTime'] = format_date(str(self._member['jobTime']))

        # 对1.xx格式进行处理，保留xx
        self._member['gender'] = self._member.get('gender', '').split(',')[-1]
        self._member['nation'] = self._member.get('nation', '').split(',')[-1]
        self._member['health'] = self._member.get('health', '').split(',')[-1]
        self._member['marriage'] = self._member.get('marriage', '').split(',')[-1]
        self._member['idType'] = self._member.get('idType', '').split(',')[-1]
        self._member['branchTime'] = self._member.get('branchTime', '').split(',')[-1]
        self._member['branchTime'] = self._member.get('branchTime', '').split(',')[-1]

    def main_function(self):
        for i in self._tabs_name:
            self._tabs_name[i]()

    def member_edu_degree(self):
        """
        学历信息
        :return:
        """
        # 获得学历sheet
        edu_degree_sheet = self._book.sheet_by_name(u'A04.学历与学位')
        for i in range(2, edu_degree_sheet.nrows):
            if edu_degree_sheet.cell_value(i, 1) == "":
                return
            else:
                edu_degree = {"eduSchoolName": edu_degree_sheet.cell_value(i, 1),
                              "eduStartingDate": format_date(str(edu_degree_sheet.cell_value(i, 2))),
                              "eduGraduateDate": format_date(str(edu_degree_sheet.cell_value(i, 3))),
                              "eduMajor": edu_degree_sheet.cell_value(i, 4),
                              "eduEducation": edu_degree_sheet.cell_value(i, 5),
                              "eduDegree": edu_degree_sheet.cell_value(i, 6),
                              "eduEducationType": edu_degree_sheet.cell_value(i, 7)}
                # 对1.xx格式进行处理，保留xx
                edu_degree['eduEducation'] = edu_degree.get('eduEducation', '').split(',')[-1]
                edu_degree['eduDegree'] = edu_degree.get('eduDegree', '').split(',')[-1]
                edu_degree['eduEducationType'] = edu_degree.get('eduEducationType', '').split(',')[-1]

                self._member["educationDegree"].append(edu_degree)

    def member_job_resumes(self):
        """
        工作履历
        :return:
        """
        # 获得工作履历sheet
        job_resumes_sheet = self._book.sheet_by_name(u'A19.工作履历')
        for i in range(2, job_resumes_sheet.nrows):
            if job_resumes_sheet.cell_value(i, 1) == "":
                return
            else:
                job_esumes = {"jobCompanyName": job_resumes_sheet.cell_value(i, 1),
                              "jobDep": job_resumes_sheet.cell_value(i, 2),
                              "jobDuties": job_resumes_sheet.cell_value(i, 3),
                              "jobTitle": job_resumes_sheet.cell_value(i, 4),
                              "jobAcademic": job_resumes_sheet.cell_value(i, 5),
                              "jobStartTime": format_date(str(job_resumes_sheet.cell_value(i, 6))),
                              "jobEndTime": format_date(str(job_resumes_sheet.cell_value(i, 7))),
                              "jobReterence": job_resumes_sheet.cell_value(i, 8)}
                self._member["jobResumes"].append(job_esumes)

    def member_professional(self):
        """
        专业技术工作
        :return:
        """
        # 获得专业技术工作sheet
        member_professional_sheet = self._book.sheet_by_name(u'A43.专业技术工作')
        for i in range(2, member_professional_sheet.nrows):
            if member_professional_sheet.cell_value(i, 1) == "":
                return
            else:
                professional_skill = {
                    "proProjectName": member_professional_sheet.cell_value(i, 1),
                    "proProjectType": member_professional_sheet.cell_value(i, 2),
                    "proProjectCompany": member_professional_sheet.cell_value(i, 3),
                    "proRolesInProject": member_professional_sheet.cell_value(i, 4),
                    "proStartDate": format_date(str(member_professional_sheet.cell_value(i, 5))),
                    "porEndDate": format_date(str(member_professional_sheet.cell_value(i, 6)))}

                # 对1.xx格式进行处理，保留xx
                professional_skill['proProjectType'] = professional_skill.get('proProjectType', '').split(',')[-1]
                professional_skill['proRolesInProject'] = professional_skill.get('proRolesInProject', '').split(',')[-1]
                self._member["professionalSkill"].append(professional_skill)

    def member_family_relation(self):
        """
        社会关系
        :return:
        """
        # 获得社会关系sheet
        family_relation_sheet = self._book.sheet_by_name(u'A79.家庭社会关系')
        for i in range(2, family_relation_sheet.nrows):
            if family_relation_sheet.cell_value(i, 1) == "":
                return
            else:
                family_relations = {
                    "familyName": family_relation_sheet.cell_value(i, 1),
                    "familyRelation": family_relation_sheet.cell_value(i, 2),
                    "familyGender": family_relation_sheet.cell_value(i, 3),
                    "familyBirthDay": format_date(str(family_relation_sheet.cell_value(i, 4))),
                    "familyCompany": family_relation_sheet.cell_value(i, 5),
                    "familyJob": family_relation_sheet.cell_value(i, 6),
                    "familyNationality": family_relation_sheet.cell_value(i, 7),
                    "familyPolitical": family_relation_sheet.cell_value(i, 8)}

                # 对1.xx格式进行处理，保留xx
                family_relations['familyRelation'] = family_relations.get('familyRelation', '').split(',')[-1]
                family_relations['familyGender'] = family_relations.get('familyGender', '').split(',')[-1]
                family_relations['familyPolitical'] = family_relations.get('familyPolitical', '').split(',')[-1]

                self._member["familyRelations"].append(family_relations)

    def member_paper(self):
        """
        主要论文著作
        :return:
        """
        # 获得主要论文著作sheet
        paper_sheet = self._book.sheet_by_name('A45.主要论文著作')
        for i in range(2, paper_sheet.nrows):
            if paper_sheet.cell_value(i, 1) == "":
                return
            else:
                paper = {
                    "paperPublications": paper_sheet.cell_value(i, 1),
                    "paperName": paper_sheet.cell_value(i, 2),
                    "paperPress": paper_sheet.cell_value(i, 3),
                    "paperAuthorSort": paper_sheet.cell_value(i, 4),
                    "paperPressDate": format_date(str(paper_sheet.cell_value(i, 5))),
                    "paperRoleDetail": paper_sheet.cell_value(i, 6)}

                # 对1.xx格式进行处理，保留xx
                paper['paperPublications'] = paper.get('paperPublications', '').split(',')[-1]
                paper['paperRoleDetail'] = paper.get('paperRoleDetail', '').split(',')[-1]

                self._member["paper"].append(paper)

    def member_achievements(self):
        """
        专业技术成果
        :return:
        """
        # 获得专业技术成果sheet
        achievements_sheet = self._book.sheet_by_name(u'A46.专业技术成果')
        for i in range(2, achievements_sheet.nrows):
            if achievements_sheet.cell_value(i, 1) == "":
                return
            else:
                achievements = {
                    "achievementsName": achievements_sheet.cell_value(i, 1),
                    "achievementsLevel": achievements_sheet.cell_value(i, 2),
                    "identificationUnit": achievements_sheet.cell_value(i, 3),
                    "achievementsRemark": achievements_sheet.cell_value(i, 4)}

                # 对1.xx格式进行处理，保留xx
                achievements['achievementsLevel'] = achievements.get('achievementsLevel', '').split(',')[-1]

                self._member["achievements"].append(achievements)

    def member_award(self):
        """
        专业技术工作获奖
        :return:
        """
        # 获得专业技术工作获奖sheet
        award_sheet = self._book.sheet_by_name(u'A49.专业技术工作获奖')
        for i in range(2, award_sheet.nrows):
            if award_sheet.cell_value(i, 1) == "":
                return
            else:
                award = {
                    "awardProjectName": award_sheet.cell_value(i, 1),
                    "awardDate": format_date(str(award_sheet.cell_value(i, 2))),
                    "awardNameAndLevel": award_sheet.cell_value(i, 3),
                    "awardRoleInProject": award_sheet.cell_value(i, 4),
                    "awardCompany": award_sheet.cell_value(i, 5),
                    "awardMemo": award_sheet.cell_value(i, 6)
                }
                self._member["award"].append(award)

    def member_patents(self):
        """
        专利情况
        :return:
        """
        # 获得专利情况sheet
        patents_sheet = self._book.sheet_by_name(u'A52.专利情况')
        for i in range(2, patents_sheet.nrows):
            if patents_sheet.cell_value(i, 1) == "":
                return
            else:
                patents = {
                    "patentName": patents_sheet.cell_value(i, 1),
                    "patentDate": format_date(str(patents_sheet.cell_value(i, 2))),
                    "patenNo": patents_sheet.cell_value(i, 3)}
                self._member["patents"].append(patents)

    def member_professor(self):
        """
        专家情况
        :return:
        """
        # 获得专家情况sheet
        professor_sheet = self._book.sheet_by_name(u'A70.专家情况')
        for i in range(2, professor_sheet.nrows):
            if professor_sheet.cell_value(i, 1) == "":
                return
            else:
                professor = {
                    "professorName": professor_sheet.cell_value(i, 1),
                    "approvalDate": format_date(str(professor_sheet.cell_value(i, 2))),
                    "approvalCompanyLevel": professor_sheet.cell_value(i, 3),
                    "approvalCompanyName": professor_sheet.cell_value(i, 4),
                    "govSubsidiesType": professor_sheet.cell_value(i, 5),
                    "subsidiesDate": format_date(str(professor_sheet.cell_value(i, 6))),
                }
                self._member["professor"].append(professor)

    def member_specialized_skill(self):
        """
        业务专长
        :return:
        """
        # 获得业务专长sheet
        specialized_skill_sheet = self._book.sheet_by_name(u'业务专长')
        for i in range(2, specialized_skill_sheet.nrows):
            if specialized_skill_sheet.cell_value(i, 1) == "":
                return
            else:
                specialized_skill = {
                    "specializedType": specialized_skill_sheet.cell_value(i, 1),
                    "specializedName": specialized_skill_sheet.cell_value(i, 2),
                    "specializedDetailName": specialized_skill_sheet.cell_value(i, 3)}
                self._member["specializedskill"].append(specialized_skill)

    def member_former_club_office(self):
        """
        社内职务
        :return:
        """
        # 获得社内职务sheet
        former_club_office_sheet = self._book.sheet_by_name(u'历任社内职务')
        for i in range(2, former_club_office_sheet.nrows):
            if former_club_office_sheet.cell_value(i, 1) == "":
                return
            else:
                former_club_office = {
                    "formerOrganizationCategory": former_club_office_sheet.cell_value(i, 1),
                    "formerOrganizationName": former_club_office_sheet.cell_value(i, 2),
                    "formerOrganizationLevel": former_club_office_sheet.cell_value(i, 3),
                    "formerOrganizationJob": former_club_office_sheet.cell_value(i, 4),
                    "formerTheTime": former_club_office_sheet.cell_value(i, 5),
                    "formerStartTime": format_date(str(former_club_office_sheet.cell_value(i, 6))),
                    "formerEndTime": format_date(str(former_club_office_sheet.cell_value(i, 7)))
                }

                # 对1.xx格式进行处理，保留xx
                former_club_office['formerOrganizationLevel'] = \
                    former_club_office.get('formerOrganizationLevel', '').split(',')[-1]

                self._member["formerClubOffice"].append(former_club_office)

    def member_social(self):
        """
        社会职务
        :return:
        """
        # 获得社会职务sheet
        social_sheet = self._book.sheet_by_name(u'政府和主要社会职务')
        for i in range(2, social_sheet.nrows):
            if social_sheet.cell_value(i, 1) == "":
                return
            else:
                social = {
                    "socialOrgType": social_sheet.cell_value(i, 1),
                    "socialOrgName": social_sheet.cell_value(i, 2),
                    "socialPositionLevel": social_sheet.cell_value(i, 3),
                    "socialPositionName": social_sheet.cell_value(i, 4),
                    "socialPeriod": social_sheet.cell_value(i, 5),
                    "socialBeginDate": format_date(str(social_sheet.cell_value(i, 6))),
                    "socialEndDate": format_date(str(social_sheet.cell_value(i, 7)))
                }

                # 对1.xx格式进行处理，保留xx
                social['socialPositionLevel'] = social.get('socialPositionLevel', '').split(',')[-1]

                self._member["social"].append(social)

    def member_social_duties(self):
        """
        其它职务
        :return:
        """
        # 获得其它职务sheet
        social_duties_sheet = self._book.sheet_by_name(u'其它社会职务')
        for i in range(2, social_duties_sheet.nrows):
            if social_duties_sheet.cell_value(i, 1) == "":
                return
            else:
                social_duties = {
                    "socialOrganizationCategory": social_duties_sheet.cell_value(i, 1),
                    "socialOrganizationLevel": social_duties_sheet.cell_value(i, 2),
                    "socialPositionLevel": social_duties_sheet.cell_value(i, 3),
                    "socialOrganizationJob": social_duties_sheet.cell_value(i, 4),
                    "socialTheTime": social_duties_sheet.cell_value(i, 5),
                    "socialStartTime": format_date(str(social_duties_sheet.cell_value(i, 6))),
                    "socialEndTime": format_date(str(social_duties_sheet.cell_value(i, 7)))
                }
                self._member["socialduties"].append(social_duties)

    def member_agency_broker(self):
        """
        入社介绍人
        :return:
        """
        # 获得入社介绍人sheet
        agency_broker_sheet = self._book.sheet_by_name(u'入社介绍人')
        for i in range(2, agency_broker_sheet.nrows):
            if agency_broker_sheet.cell_value(i, 1) == "":
                return
            else:
                agency_broker = {
                    "agencyName": agency_broker_sheet.cell_value(i, 1),
                    "agencyCompany": agency_broker_sheet.cell_value(i, 2),
                    "agencyJob": agency_broker_sheet.cell_value(i, 3),
                    "agencyRelationShip": agency_broker_sheet.cell_value(i, 4)}
                self._member["agencybroker"].append(agency_broker)

    def save_member(self, file_name):
        """
        保存社员信息
        :return:
        """
        query_name = self._member["name"]
        query_birthday = self._member["birthday"]
        obj = {
            "selector": {
                "name": {"$eq": query_name},
                "birthday": {"$eq": query_birthday}
            },
            "fields": ["_id", "name", "birthday"]
        }
        request = couch_db.post(r'/jsmm/_find/', obj)
        member = json.loads(request.body.decode('utf-8'))
        result = {}
        if len(member["docs"]):
            memberInfo = member["docs"]
            # 根据姓名和出生日期判断重复数据
            msg = {"success": False, "fileName": file_name, "errorContent": ErrorType.FILEREPEATERROR.value}
            return msg
        else:
            try:
                # 判断组织机构树中是否已经存在该机构名称，如果不存在则添加
                branch = self._member.get('branch', '')
                if branch:
                    response = couch_db.get(r'/jsmm/_design/organ/_view/getOrgan')
                    organ_content = json.loads(response.body.decode('utf-8'))
                    organ_row = organ_content['rows'][0]
                    organ_value = organ_row['value']
                    organ_cy = (((organ_value['organ'])[0])['children'])[0]

                    organ = {'id': branch, 'text': branch}

                    if 'children' not in organ_cy:
                        organ_cy['children'] = list()

                    # 如果支社名称不存在，则添加支社
                    if organ not in organ_cy['children']:
                        organ_cy['children'].append(organ)
                        couch_db.put(r'/jsmm/%(id)s' % {"id": organ_value['_id']}, organ_value)

                # 保存社员信息
                self._member["retireTime"] = get_retire_time(self._member["birthday"], self._member["gender"])
                self._member["lost"] = "否"
                self._member["stratum"] = "否"
                couch_db.post(r'/jsmm/', self._member)
                result = {'success': True}
            except Exception as e:
                print(Exception, ":", e)
                # 日期格式错误
                result = {'success': False, "fileName": file_name, 'errorContent': ErrorType.DATAFORMATEERROR.value}
            finally:
                return result

    @property
    def member(self):
        return self._member

# if __name__ == "__main__":
#     import sys
#     sys.path[:0] = ['app', 'lib']
#     from couchdb import CouchDB
#     couch_db = CouchDB('http://127.0.0.1:5984')
#     member_info_importer = MemberInfoImporter('inbox/殷大发的信息.xls')
#     member_info_importer.get_basic_info()
#     member_info_importer.main_function()
#     member_info_importer.save_member()
