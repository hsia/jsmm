#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright lixia@ccrise.com
'''
import uuid
from xlrd import open_workbook

# from commons import couch_db, make_uuid


def make_uuid():
    '''
    生成随机的UUID，并返回16进制字符串
    '''
    return uuid.uuid4().hex


class MemberInfoImporter():
    '''
    导入社员信息。
    '''

    def __init__(self, path):
        '''
        打开一个包含社员基本信息的Excel文件。
        '''
        self._book = open_workbook(path)
        self._member = {
            'type': 'member',
            '_id': make_uuid()
        }
        print(r'正在处理%(path)s' % {'path': path})

    def get_basic_info(self):
        '''
        获取"A01.基本信息页"
        '''
        mapper = {'姓名': 'name',
                  '外文姓名': 'foreignName',
                  '曾用名': 'usedName',
                  '性别': 'gender',
                  '出生日期': 'birthday',
                  '籍贯': 'nativePlace',
                  '出生地': 'birthPlace',
                  '民族': 'nation',
                  '健康状态': 'health',
                  '婚姻状态': 'marriage',
                  '公民身份证号码': 'idCard',
                  '有效证件类别': 'idType',
                  '证件号码': 'idNo',
                  '所属支社': 'branch',
                  '所属基层组织名称': 'organ',
                  '入社时间': 'branchTime',
                  '党派交叉': 'partyCross',
                  '单位名称': 'companyName',
                  '参加工作时间': 'jobTime',
                  '工作部门': 'department',
                  '是否办理退休手续': 'retire',
                  '职务': 'duty',
                  '职称': 'jobTitle',
                  '学术职务': 'academic',
                  '家庭地址': 'homeAddress',
                  '家庭地址邮编': 'homePost',
                  '家庭电话': 'homeTel',
                  '单位地址': 'companyAddress',
                  '单位地址邮编': 'companyPost',
                  '通信地址': 'commAddress',
                  '通信地址邮编': 'commPost',
                  '移动电话': 'mobile',
                  '电子信箱': 'email',
                  '单位电话': 'companyTel',
                  '爱好': 'hobby'}

        sheet = self._book.sheet_by_name(r'A01.基本信息页')
        for row_index in range(2, sheet.nrows):
            name = sheet.cell_value(row_index, 1)
            if name in mapper:
                self._member[mapper[name]] = sheet.cell_value(row_index, 2)
        print(self._member)

    def save_member(self):
        '''
        保存社员信息
        '''
        pass

if __name__ == "__main__":
    member_info_importer = MemberInfoImporter('../inbox/示例—社员信息采集-黄某某.xls')
    member_info_importer.get_basic_info()
    member_info_importer.save_member()
