#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import tornado.web

from commons import couch_db, formatter_time
from lib import tornado_utils, ErrorType


@tornado_utils.bind_to(r'/members/([0-9a-f]+)')
class MemberHandler(tornado.web.RequestHandler):
    """
    MemberHandler
    """

    def get(self, member_id):
        """
        获取_id为member_id的member对象。
        """
        query = {'keys': [member_id]}
        documents_response = couch_db.post(
            r'/jsmm/_design/documents/_view/by_memberid', query)
        documents = json.loads(documents_response.body.decode('utf-8'))
        member_response = couch_db.get(r'/jsmm/%(id)s' % {'id': member_id})
        member = json.loads(member_response.body.decode('utf-8'))
        member['researchReport'] = [doc['value'] for doc in documents[
            'rows'] if doc['value']['docType'] == 'researchReport']
        member['unitedTheory'] = [doc['value'] for doc in documents[
            'rows'] if doc['value']['docType'] == 'unitedTheory']
        member['politicsInfo'] = [doc['value'] for doc in documents[
            'rows'] if doc['value']['docType'] == 'politicsInfo']
        member['propaganda'] = [doc['value'] for doc in documents[
            'rows'] if doc['value']['docType'] == 'propaganda']
        # 处理文档上传日期，使用空格代替T
        for researchReport in member.get('researchReport', []):
            researchReport['fileUploadTime'] = (researchReport.get('fileUploadTime')).replace('T', ' ')
        for researchReport in member.get('unitedTheory', []):
            researchReport['fileUploadTime'] = (researchReport.get('fileUploadTime')).replace('T', ' ')
        for researchReport in member.get('politicsInfo', []):
            researchReport['fileUploadTime'] = (researchReport.get('fileUploadTime')).replace('T', ' ')
        for researchReport in member.get('propaganda', []):
            researchReport['fileUploadTime'] = (researchReport.get('fileUploadTime')).replace('T', ' ')

        member.get('researchReport', []).sort(key=lambda k: k.get('fileUploadTime', ''), reverse=True)
        member.get('unitedTheory', []).sort(key=lambda k: k.get('fileUploadTime', ''), reverse=True)
        member.get('politicsInfo', []).sort(key=lambda k: k.get('fileUploadTime', ''), reverse=True)
        member.get('propaganda', []).sort(key=lambda k: k.get('fileUploadTime', ''), reverse=True)
        self.write(member)

    def put(self, member_id):
        """
        修改_id为member_id的member对象。
        """
        # 获得前台对象#
        member_updated = json.loads(self.request.body.decode('utf-8'))
        try:
            formatter_time(member_updated.get('birthday', ''), '%Y-%m-%d', '%Y-%m-%d')
            formatter_time(member_updated.get('branchTime', ''), '%Y-%m-%d', '%Y-%m-%d')
            formatter_time(member_updated.get('jobTime', ''), '%Y-%m-%d', '%Y-%m-%d')

            # 判断各个页签中的日期格式是否正确
            if member_updated.get('educationDegree', []):
                for educationDegree in member_updated.get('educationDegree'):
                    formatter_time(educationDegree.get('eduStartingDate', ''), '%Y-%m-%d', '%Y-%m-%d')
                    formatter_time(educationDegree.get('eduGraduateDate', ''), '%Y-%m-%d', '%Y-%m-%d')

            if member_updated.get('jobResumes', []):
                for jobResumes in member_updated.get('jobResumes'):
                    formatter_time(jobResumes.get('jobStartTime', ''), '%Y-%m-%d', '%Y-%m-%d')
                    formatter_time(jobResumes.get('jobEndTime', ''), '%Y-%m-%d', '%Y-%m-%d')

            if member_updated.get('familyRelations', []):
                for familyRelations in member_updated.get('familyRelations'):
                    formatter_time(familyRelations.get('familyBirthDay', ''), '%Y-%m-%d', '%Y-%m-%d')

            if member_updated.get('paper', []):
                for paper in member_updated.get('paper'):
                    formatter_time(paper.get('paperPressDate', ''), '%Y-%m-%d', '%Y-%m-%d')

            if member_updated.get('award', []):
                for award in member_updated.get('award'):
                    formatter_time(award.get('awardDate', ''), '%Y-%m-%d', '%Y-%m-%d')

            if member_updated.get('patents', []):
                for patents in member_updated.get('patents'):
                    formatter_time(patents.get('patentDate', ''), '%Y-%m-%d', '%Y-%m-%d')

            if member_updated.get('professionalSkill', []):
                for professionalSkill in member_updated.get('professionalSkill'):
                    formatter_time(professionalSkill.get('proStartDate', ''), '%Y-%m-%d', '%Y-%m-%d')
                    formatter_time(professionalSkill.get('porEndDate', ''), '%Y-%m-%d', '%Y-%m-%d')

            if member_updated.get('professor', []):
                for professor in member_updated.get('professor'):
                    formatter_time(professor.get('subsidiesDate', ''), '%Y-%m-%d', '%Y-%m-%d')
                    formatter_time(professor.get('approvalDate', ''), '%Y-%m-%d', '%Y-%m-%d')

            if member_updated.get('formerClubOffice', []):
                for formerClubOffice in member_updated.get('formerClubOffice'):
                    formatter_time(formerClubOffice.get('formerStartTime', ''), '%Y-%m-%d', '%Y-%m-%d')
                    formatter_time(formerClubOffice.get('formerEndTime', ''), '%Y-%m-%d', '%Y-%m-%d')

            if member_updated.get('social', []):
                for social in member_updated.get('social'):
                    formatter_time(social.get('socialBeginDate', ''), '%Y-%m-%d', '%Y-%m-%d')
                    formatter_time(social.get('socialEndDate', ''), '%Y-%m-%d', '%Y-%m-%d')

            if member_updated.get('socialDuties', []):
                for socialDuties in member_updated.get('socialDuties'):
                    formatter_time(socialDuties.get('socialStartTime', ''), '%Y-%m-%d', '%Y-%m-%d')
                    formatter_time(socialDuties.get('socialEndTime', ''), '%Y-%m-%d', '%Y-%m-%d')

            if member_updated.get('participatePerformance', []):
                for participatePerformance in member_updated.get('participatePerformance'):
                    formatter_time(participatePerformance.get('perfDate', ''), '%Y-%m-%d', '%Y-%m-%d')

            if member_updated.get('politicsResume', []):
                for politicsResume in member_updated.get('politicsResume'):
                    formatter_time(politicsResume.get('resumeDate', ''), '%Y-%m-%d', '%Y-%m-%d')

            # 根据memeber_id，查询数据库中的memeber对象
            response = couch_db.get(r'/jsmm/%(id)s' % {'id': member_id})
            member = json.loads(response.body.decode('utf-8'))
            # 将前台数据赋予后台对象，然后将后台对象保存。
            member.update(member_updated)
            # 将document中的member数据更新

            query = {'keys': [member_id]}
            documents_response = couch_db.post(
                r'/jsmm/_design/documents/_view/by_memberid', query)
            documents = json.loads(documents_response.body.decode('utf-8'))

            for doc in documents['rows']:
                doc['value']['name'] = member['name']
                doc['value']['branch'] = member['branch']
                doc['value']['organ'] = member['organ']
                couch_db.put(r'/jsmm/%(id)s' %
                             {'id': doc['value']['_id']}, doc['value'])

            couch_db.put(r'/jsmm/%(id)s' % {'id': member_id}, member)
            response = {'success': 'true'}
        except Exception as e:
            print(e)
            response = {"success": "false", "content": ErrorType.DATAFORMATEERROR1.value}

        self.write(response)

    def delete(self, member_id):
        """
        删除_id为member_id的member对象。
        """
        # 通过HEAD方法查询Etag（即_rev）。
        response = couch_db.head(r'/jsmm/%(id)s' % {'id': member_id})
        # 从返回的headers中查找包含"Etag"的数据，取第一条，并去除头尾的双引号。
        rev = response.headers.get_list('Etag')[0][1:-1]
        # couch_db.delete(r'/jsmm/%(id)s?rev=%(rev)s' % {'id': member_id, 'rev': rev})
        query = {'keys': [member_id]}
        documents_response = couch_db.post(
            r'/jsmm/_design/documents/_view/by_memberid', query)
        documents = json.loads(documents_response.body.decode('utf-8'))

        for doc in documents['rows']:
            couch_db.delete(r'/jsmm/%(id)s?rev=%(rev)s' %
                            {'id': doc['value']['_id'], 'rev': doc['value']['_rev']})

        couch_db.delete(r'/jsmm/%(id)s?rev=%(rev)s' %
                        {'id': member_id, 'rev': rev})

        response = {'success': 'true'}
        self.write(response)
