#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import urllib

import tornado.web

import tornado_utils
from commons import couch_db


@tornado_utils.bind_to(r'/members/([0-9a-f]+)')
class MemberHandler(tornado.web.RequestHandler):
    """
    MemberHandler
    """

    def get(self, member_id):
        """
        获取_id为member_id的member对象。
        """
        query = {"keys": [member_id]};
        responseDocuments = couch_db.post(r'/jsmm/_design/documents/_view/by_memberid', query)

        documents = json.loads(responseDocuments.body.decode("utf-8"))
        responseMemberInfo = couch_db.get(r'/jsmm/%(id)s' % {"id": member_id})
        member = json.loads(responseMemberInfo.body.decode('utf-8'));

        departmentReport = [];
        departmentInfo = [];
        speechesText = [];
        for doc in documents["rows"]:
            if 'departmentReport' == doc["value"]["docType"]:
                departmentReport.append(doc["value"])
            elif "departmentInfo" in doc["value"]["docType"]:
                departmentInfo.append(doc["value"])
            elif "speechesText" in doc["value"]["docType"]:
                speechesText.append(doc["value"])
        member['departmentReport'] = departmentReport;
        member['departmentInfo'] = departmentInfo;
        member['speechesText'] = speechesText;

        self.write(member)

    def put(self, member_id):
        """
        修改_id为member_id的member对象。
        """
        # 获得前台对象#
        member_updated = json.loads(self.request.body.decode('utf-8'))
        # 根据memeber_id，查询数据库中的memeber对象
        response = couch_db.get(r'/jsmm/%(id)s' % {'id': member_id})
        member = json.loads(response.body.decode('utf-8'))
        # 将前台数据赋予后台对象，然后将后台对象保存。
        member.update(member_updated)
        # 将document中的member数据更新

        query = {"keys": [member_id]};
        responseDocuments = couch_db.post(r'/jsmm/_design/documents/_view/by-memberid', query)
        documents = json.loads(responseDocuments.body.decode('utf-8'));

        for doc in documents["rows"]:
            doc["value"]['name'] = member['name']
            doc["value"]['branch'] = member['branch']
            doc["value"]['organ'] = member['organ']
            couch_db.put(r'/jsmm/%(id)s' % {"id": doc["value"]['_id']}, doc["value"])

        couch_db.put(r'/jsmm/%(id)s' % {"id": member_id}, member)
        response = {"success": "true"}
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
        query = {"keys": [member_id]};
        responseDocuments = couch_db.post(r'/jsmm/_design/documents/_view/by-memberid', query)
        documents = json.loads(responseDocuments.body.decode('utf-8'));

        for doc in documents["rows"]:
            couch_db.delete(r'/jsmm/%(id)s?rev=%(rev)s' % {'id': doc["value"]["_id"], 'rev': doc["value"]["_rev"]})

        couch_db.delete(r'/jsmm/%(id)s?rev=%(rev)s' % {'id': member_id, 'rev': rev})

        response = {"success": "true"}
        self.write(response)
