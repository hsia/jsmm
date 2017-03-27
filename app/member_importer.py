#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright lixia@ccrise.com
'''
import uuid
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
    if date_str == u'至今':           # '至今'
        return ''
    splited = date_str.split('.')   # 'YYYY', 'YYYY.MM'或'YYYY.MM.DD'
    if len(splited) == 1:           # ['YYYY']
        splited += ['01', '01']     # ['YYYY', '01', '01']
    elif len(splited) == 2:         # ['YYYY', 'MM']
        splited.append('01')        # ['YYYY', 'MM', '01']
    return '-'.join(splited)        # 'YYYY-MM-DD'


def import_info(file_info):
    member_info_importer = MemberInfoImporter(file_info['path'])
    member_info_importer.get_basic_info()
    member_info_importer.main_function()
    return member_info_importer.save_member()



class MemberInfoImporter():
    """
    导入社员信息。
    """
    def __init__(self, path):
        """
        打开一个包含社员基本信息的Excel文件。
        :param path:
        """
        self.current_row = 19
        self._book = open_workbook(path)
        self._sheet = self._book.sheet_by_index(0)
        self._member = {
            'type': 'member',
            '_id': make_uuid(),
            'educationDegree': [],      # 学历信息       1
            'jobResumes': [],           # 工作履历       1
            'professionalSkill': [],    # 专业技术工作   1
            'familyRelations': [],      # 社会关系       1
            'paper': [],                # 主要论文著作   1
            'achievements': [],         # 专业技术成果   1
            'award': [],                # 获奖情况       1
            'patents': [],              # 专利情况       1
            'professor': [],            # 专家情况       0
            'specializedskill': [],     # 业务专长       1
            'formerClubOffice': [],     # 社内职务       0
            'social': [],               # 社会职务       0
            'socialduties': [],         # 其它职务       0
            'agencybroker': []          # 入社介绍人     1
        }
        self._tabs_name = {
            u"学历信息": self.member_edu_degree,             # 学历信息
            u"工作履历": self.member_job_esumes,             # 工作履历
            u"专业技术工作": self.member_professional,       # 专业技术工作
            u"社会关系": self.member_family_relation,        # 社会关系
            u"主要论文著作": self.member_paper,              # 主要论文著作
            u"专业技术成果": self.member_achievements,       # 专业技术成果
            u"获奖情况": self.member_award,                  # 获奖情况
            u"专利情况": self.member_patents,                # 专利情况
            u"专家情况": self.member_professor,              # 专家情况
            u"业务专长": self.member_specialized_skill,      # 业务专长
            u"社内职务": self.member_former_club_office,     # 社内职务
            u"社会职务": self.member_social,                 # 社会职务
            u"其它职务": self.member_social_duties,          # 其它职务
            u"入社介绍人": self.member_agency_broker         # 入社介绍人
        }
       # print(r'正在处理%(path)s' % {'path': path})

    def get_basic_info(self):
        """
        获取"基本信息页"
        :return:
        """
        mapper = {
            (1, 1): "name",                 # 姓名
            (1, 3): "gender",               # 性别
            (1, 5): "nativePlace",          # 籍贯
            (2, 1): "nation",               # 民族
            (2, 3): "birthPlace",           # 出生地
            (2, 5): "birthday",             # 出生日期
            (3, 1): "foreignName",          # 外文姓名
            (3, 4): "usedName",             # 曾用名
            (4, 1): "health",               # 健康状态
            (4, 4): "marriage",             # 婚姻状态
            (5, 1): "branch",               # 所属支社
            (5, 4): "organ",                # 所属基层组织名称
            (6, 1): "branchTime",           # 入社时间
            (6, 4): "partyCross",           # 党派交叉
            (7, 1): "companyName",          # 单位名称
            (7, 4): "department",           # 工作部门
            (8, 1): "duty",                 # 职务
            (8, 4): "jobTitle",             # 职称
            (9, 1): "academic",             # 学术职务
            (9, 4): "jobTime",              # 参加工作时间
            (9, 8): "retire",               # 是否办理退休手续
            (10, 1): "idCard",              # 公民身份证号码
            (10, 4): "idType",              # 有效证件类别
            (10, 8): "idNo",                # 证件号码
            (11, 1): "homeAddress",         # 家庭地址
            (11, 5): "homePost",            # 家庭地址邮编
            (12, 1): "companyAddress",      # 单位地址
            (12, 5): "companyPost",         # 单位地址邮编
            (13, 1): "commAddress",         # 通信地址
            (13, 5): "commPost",            # 通信地址邮编
            (14, 1): "mobile",              # 移动电话
            (14, 5): "homeTel",             # 家庭电话
            (15, 1): "email",               # 电子信箱
            (15, 5): "companyTel",          # 单位电话
            (16, 1): "hobby",               # 爱好
            (17, 1): "speciality"           # 专长
        }

        for key in mapper.keys():
            self._member[mapper[key]] = self._sheet.cell_value(key[0], key[1])
        self._member['branchTime'] = format_date(str(self._member['branchTime']))
        self._member['birthday'] = format_date(str(self._member['birthday']))
        self._member['jobTime'] = format_date(str(self._member['jobTime']))

    def main_function(self):
        for row_index in range(self.current_row, self._sheet.nrows):
            name = self._sheet.cell_value(row_index, 0)
            if name in self._tabs_name:
                self._tabs_name[name](row_index+2)

    def member_edu_degree(self, row_index):
        """
        学历信息
        :param row_index:
        :return:
        """
        for i in range(row_index, self._sheet.nrows):
            self.current_row = i
            if self._sheet.cell_value(i, 0) == "":
                return
            else:
                [start_time, end_time] = self._sheet.cell_value(i, 2).split(' - ')

                edu_degree = {"eduSchoolName": self._sheet.cell_value(i, 0),
                             "eduStartingDate": format_date(start_time),
                             "eduGraduateDate": format_date(end_time),
                             "eduMajor": self._sheet.cell_value(i, 4),
                             "eduEducation": self._sheet.cell_value(i, 6),
                             "eduDegree": self._sheet.cell_value(i, 7),
                             "eduEducationType": self._sheet.cell_value(i, 9)}

                self._member["educationDegree"].append(edu_degree)

    def member_job_esumes(self, row_index):
        """
        工作履历
        :param row_index:
        :return:
        """
        for i in range(row_index, self._sheet.nrows):
            self.current_row = i
            if self._sheet.cell_value(i, 0) == "":
                return
            else:
                [start_time, end_time] = self._sheet.cell_value(i, 7).split(' - ')

                job_esumes = {"jobCompanyName": self._sheet.cell_value(i, 0),
                              "jobDep": self._sheet.cell_value(i, 2),
                              "jobDuties": self._sheet.cell_value(i, 4),
                              "jobTitle": self._sheet.cell_value(i, 5),
                              "jobAcademic": self._sheet.cell_value(i, 6),
                              "jobStartTime": format_date(start_time),
                              "jobEndTime": format_date(end_time),
                              "jobReterence": self._sheet.cell_value(i, 9)}
                self._member["jobResumes"].append(job_esumes)

    def member_professional(self, row_index):
        """
        专业技术工作
        :param row_index:
        :return:
        """
        for i in range(row_index, self._sheet.nrows):
            self.current_row = i
            if self._sheet.cell_value(i, 0) == "":
                return
            else:
                [start_time, end_time] = self._sheet.cell_value(i, 8).split(' - ')

                professional_skill = {
                              "proProjectName": self._sheet.cell_value(i, 0),
                              "proProjectType": self._sheet.cell_value(i, 4),
                              "proProjectCompany": self._sheet.cell_value(i, 5),
                              "proRolesInProject": self._sheet.cell_value(i, 7),
                              "proStartDate": format_date(start_time),
                              "porEndDate": format_date(end_time)}
                self._member["professionalSkill"].append(professional_skill)

    def member_family_relation(self, row_index):
        """
        社会关系
        :param row_index:
        :return:
        """
        for i in range(row_index, self._sheet.nrows):
            self.current_row = i
            if self._sheet.cell_value(i, 0) == "":
                return
            else:
                family_relations = {
                              "familyName": self._sheet.cell_value(i, 0),
                              "familyRelation": self._sheet.cell_value(i, 1),
                              "familyGender": self._sheet.cell_value(i, 2),
                              "familyBirthDay": format_date(str(self._sheet.cell_value(i, 3))),
                              "familyCompany": self._sheet.cell_value(i, 4),
                              "familyJob": self._sheet.cell_value(i, 6),
                              "familyNationality": self._sheet.cell_value(i, 7),
                              "familyPolitical": self._sheet.cell_value(i, 8)}
                self._member["familyRelations"].append(family_relations)

    def member_paper(self, row_index):
        """
        主要论文著作
        :param row_index:
        :return:
        """
        for i in range(row_index, self._sheet.nrows):
            self.current_row = i
            if self._sheet.cell_value(i, 0) == "":
                return
            else:
                paper = {
                              "paperPublications": self._sheet.cell_value(i, 0),
                              "paperName": self._sheet.cell_value(i, 1),
                              "paperPress": self._sheet.cell_value(i, 4),
                              "paperAuthorSort": self._sheet.cell_value(i, 7),
                              "paperPressDate": format_date(str(self._sheet.cell_value(i, 8))),
                              "paperRoleDetail": self._sheet.cell_value(i, 9)}
                self._member["paper"].append(paper)

    def member_achievements(self, row_index):
        """
        专业技术成果
        :param row_index:
        :return:
        """
        for i in range(row_index, self._sheet.nrows):
            self.current_row = i
            if self._sheet.cell_value(i, 0) == "":
                return
            else:
                achievements = {
                              "achievementsName": self._sheet.cell_value(i, 0),
                              "achievementsLevel": self._sheet.cell_value(i, 3),
                              "identificationUnit": self._sheet.cell_value(i, 6),
                              "achievementsRemark": self._sheet.cell_value(i, 8)}
                self._member["achievements"].append(achievements)

    def member_patents(self, row_index):
        """
        专利情况
        :param row_index:
        :return:
        """
        for i in range(row_index, self._sheet.nrows):
            self.current_row = i
            if self._sheet.cell_value(i, 0) == "":
                return
            else:
                patents = {
                              "patentName": self._sheet.cell_value(i, 0),
                              "patentDate": format_date(str(self._sheet.cell_value(i, 4))),
                              "patenNo": self._sheet.cell_value(i, 6)}
                self._member["patents"].append(patents)

    def member_specialized_skill(self, row_index):
        """
        业务专长
        :param row_index:
        :return:
        """
        for i in range(row_index, self._sheet.nrows):
            self.current_row = i
            if self._sheet.cell_value(i, 0) == "":
                return
            else:
                specialized_skill = {
                              "specializedType": self._sheet.cell_value(i, 0),
                              "specializedName": self._sheet.cell_value(i, 2),
                              "specializedDetailName": self._sheet.cell_value(i, 5)}
                self._member["specializedskill"].append(specialized_skill)

    def member_agency_broker(self, row_index):
        """
        入社介绍人
        :param row_index:
        :return:
        """
        for i in range(row_index, self._sheet.nrows):
            self.current_row = i
            if self._sheet.cell_value(i, 0) == "":
                return
            else:
                agency_broker = {
                              "agencyName": self._sheet.cell_value(i, 0),
                              "agencyCompany": self._sheet.cell_value(i, 2),
                              "agencyJob": self._sheet.cell_value(i, 5),
                              "agencyRelationShip": self._sheet.cell_value(i, 7)}
                self._member["agencybroker"].append(agency_broker)

    def member_award(self, row_index):
        """
        工作获奖
        :param row_index:
        :return:
        """
        for i in range(row_index, self._sheet.nrows):
            self.current_row = i
            if self._sheet.cell_value(i, 0) == "":
                return
            else:
                award = {
                    "awardProjectName": self._sheet.cell_value(i, 0),
                    "awardDate": format_date(str(self._sheet.cell_value(i, 3))),
                    "awardNameAndLevel": self._sheet.cell_value(i, 4),
                    "awardRoleInProject": self._sheet.cell_value(i, 5),
                    "awardCompany": self._sheet.cell_value(i, 6),
                    "awardMemo": self._sheet.cell_value(i, 8)
                }
                self._member["award"].append(award)

    def member_professor(self, row_index):
        """
        专家情况
        :param row_index:
        :return:
        """
        for i in range(row_index, self._sheet.nrows):
            self.current_row = i
            if self._sheet.cell_value(i, 0) == "":
                return
            else:
                professor = {}
                self._member["professor"].append(professor)

    def member_former_club_office(self, row_index):
        """
        社内职务
        :param row_index:
        :return:
        """
        for i in range(row_index, self._sheet.nrows):
            self.current_row = i
            if self._sheet.cell_value(i, 0) == "":
                return
            else:
                former_club_office = {}
                self._member["formerClubOffice"].append(former_club_office)

    def member_social(self, row_index):
        """
        社会职务
        :param row_index:
        :return:
        """
        for i in range(row_index, self._sheet.nrows):
            self.current_row = i
            if self._sheet.cell_value(i, 0) == "":
                return
            else:
                social = {}
                self._member["social"].append(social)

    def member_social_duties(self, row_index):
        """
        其它职务
        :param row_index:
        :return:
        """
        for i in range(row_index, self._sheet.nrows):
            self.current_row = i
            if self._sheet.cell_value(i, 0) == "":
                return
            else:
                social_duties = {}
                self._member["socialduties"].append(social_duties)

    def save_member(self):
        """
        保存社员信息
        :return:
        """
        query_name = self._member["name"]
        query_id_card = self._member["idCard"]
        obj = {
            "selector": {
                "name": {"$eq": query_name},
                "idCard": {"$eq": query_id_card}
            },
            "fields": ["_id", "name", "idCard"]
        }
        request = couch_db.post(r'/jsmm/_find/', obj)
        member = json.loads(request.body.decode('utf-8'))
        if len(member["docs"]):
            memberInfo = member["docs"]
            msg = {"success": False, "name": memberInfo[0]["name"], "idCard": memberInfo[0]["idCard"]}
            return msg
        else:
            self._member["retireTime"] = get_retire_time(self._member["birthday"], self._member["gender"])
            self._member["lost"] = "否"
            self._member["stratum"] = "否"
            couch_db.post(r'/jsmm/', self._member)
            return {"success": True}


# if __name__ == "__main__":
#     import sys
#     sys.path[:0] = ['app', 'lib']
#     from couchdb import CouchDB
#     couch_db = CouchDB('http://127.0.0.1:5984')
#     member_info_importer = MemberInfoImporter('inbox/殷大发的信息.xls')
#     member_info_importer.get_basic_info()
#     member_info_importer.main_function()
#     member_info_importer.save_member()
