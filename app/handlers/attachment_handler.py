#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright lixia@ccrise.com
'''
import json
import os.path
import urllib
import uuid
import time

import tornado.web
from tornado.httputil import HTTPHeaders

import tornado_utils
from commons import couch_db, make_uuid


@tornado_utils.bind_to(r'/document/([0-9a-f]+)/(.+)')
class AttachmentHandler(tornado.web.RequestHandler):
    """附件处理类

    URL: '/document/<document_id>/<attachment_name>'
    """

    def _parse_header(self, response):
        """获取附件的状态、大小、文件类型信息。

        返回：(<status_code>, <content_length>, <content_type>)
        """
        # status_code = response.headers.get_list('HTTP/1.1')[0][1:-1]
        print(response.code)
        status_code = str(response.code)
        content_length = 0
        content_type = 0
        if response.code == 200:
            content_length = response.headers.get_list('Content-Length')[0][1:-1]
            content_type = response.headers.get_list('Content-Type')[0][1:-1]
        return (status_code, content_length, content_type)

    def head(self, document_id, attachment_name):
        """获取附件的状态、大小、文件类型信息。

        返回：
        {
            "success": <'true'/'false'>,      # 仅当statusCode为200时为'true'
            "statusCode": <status_code>,      # 200, 304, 401, 404
            "contentLength": <content_length>,
            "contentType": <content-type>
        }
        """
        response = couch_db.head(r'/jsmm/%(document_id)s/%(attachment_name)s' %
                                 {'document_id': document_id, 'attachment_name': attachment_name})
        (status_code, content_length, content_type) = self._parse_header(response)
        output = {'statusCode': status_code,
                  'contentLength': content_length,
                  'contentType': content_type}
        if status_code.startswith('200'):
            self.write(output.update({'success': 'true'}))
        else:
            self.write(output.update({'success': 'false'}))

    def get(self, document_id, attachment_name):
        """获取附件内容

        返回：
        {
            "success": <'true'/'false'>,      # 仅当statusCode为200时为'true'
            "statusCode": <status_code>,      # 200, 304, 401, 404
            "contentLength": <content_length>,
            "contentType": <content_type>,
            "body": <response.body>           # 仅当statusCode为200时提供
        }
        """
        response = couch_db.get(r'/jsmm/%(document_id)s/%(attachment_name)s' %
                                {'document_id': document_id, 'attachment_name': attachment_name})

        (status_code, content_length, content_type) = self._parse_header(response)
        output = {'statusCode': status_code,
                  'contentLength': content_length,
                  'contentType': content_type}
        if status_code.startswith('200'):
            self.set_header('Content-Type', content_type)
            self.set_header('Content-Disposition',
                            'attachment; filename=' + urllib.parse.quote(attachment_name, "utf-8"))
            self.write(response.body)
        else:
            self.set_header('Content-Type', 'application/json')
            output.update({'success': 'false'})
            self.write(json.dumps(output))

    def put(self, document_id, attachment_name):
        """保存附件

        如果保存任何一个附件时出现错误，返回：{'success': 'false', 'errors': <errors>}
        如果全部保存成功，返回：{'success': 'true'}
        """
        # 前端file input的name属性应指定为"docs"。
        # 接收到的文件列表结构为：{'docs': [{'filename': <filename>, 'body': <body>,
        # 'content_type': <content_type>}]}
        docs = self.request.files['docs']
        # 格式为：[{'filename': <filename>, 'error': <error>, 'reason': <reason>}]
        errors = []
        for doc in docs:
            body = doc['body']
            content_type = doc['content_type']
            # 每次保存附件后，文档的rev都会变
            head_response = couch_db.head(r'/jsmm/%(document_id)s' %
                                          {'document_id': document_id})
            rev = head_response.headers.get_list('Etag')[0][1:-1]
            put_response = couch_db.put(r'/jsmm/%(document_id)s/%(attachment_name)s?rev=%(rev)s' %
                                        {'document_id': document_id,
                                         'attachment_name': attachment_name,
                                         'rev': rev},
                                        body, content_type)
            status_code = self._parse_header(put_response)[0]
            if status_code.startswith('4'):  # 400, 401, 404, 409
                error = json.loads(put_response.body.decode('utf-8'))
                errors.append({'filename': doc['filename']}.update(error))
        if len(errors) > 0:
            self.write({'success': 'false', 'errors': errors})
        else:
            self.write({'success': 'true'})

    def delete(self, document_id, attachment_name):
        """删除附件

        返回：
        {
            "success": <'true'/'false'>,  # 当statusCode为200, 202时为'true'
            "error": <error>              # 当statusCode为400, 401, 404, 409时
        }
        """
        head_response = couch_db.head(r'/jsmm/%(document_id)s' %
                                      {'document_id': document_id})
        rev = head_response.headers.get_list('Etag')[0][1:-1]
        delete_response = couch_db.delete(r'/jsmm/%(document_id)s/%(attachment_name)s?rev=%(rev)s' %
                                          {'document_id': document_id,
                                           'attachment_name': attachment_name,
                                           'rev': rev})
        status_code = self._parse_header(delete_response)[0]
        if status_code.startswith('4'):  # 400, 401, 404, 409
            error = json.loads(delete_response.body.decode('utf-8'))
            self.write({'success': 'false', 'error': error})
        else:
            self.write({'success': 'true'})

    def post(self, member_id, doc_type):

        responseMember = couch_db.get(r'/jsmm/%(member_id)s' % {"member_id": member_id})
        memberInDb = json.loads(responseMember.body.decode('utf-8'))

        docs = self.request.files['docs']
        docName = docs[0]['filename'];

        documentInfo = {
            '_id': make_uuid(),
            'memberId': memberInDb['_id'],
            'name': memberInDb['name'],
            'type': 'document',
            'branch': memberInDb['branch'],
            'organ': memberInDb['organ'],
            'fileUploadTime': time.strftime("%Y-%m-%d", time.localtime()),
            'docType': doc_type,
            'fileName': docName
        }

        documentResponse = couch_db.post(r'/jsmm/', documentInfo)

        result = json.loads(documentResponse.body.decode('utf-8'))
        document_id = result["id"];

        if doc_type == 'departmentReport':
            if ('departmentReport' not in memberInDb):
                memberInDb['departmentReport'] = []
            memberInDb['departmentReport'].append(document_id)
        elif doc_type == 'departmentInfo':
            if ('departmentInfo' not in memberInDb):
                memberInDb['departmentInfo'] = []
            memberInDb['departmentInfo'].append(document_id)
        elif doc_type == 'speechesText':
            if ('speechesText' not in memberInDb):
                memberInDb['speechesText'] = []
            memberInDb['speechesText'].append(document_id)

        responseMemberPut = couch_db.put(r'/jsmm/%(id)s' % {"id": member_id}, memberInDb)

        return self.put(document_id, docName);