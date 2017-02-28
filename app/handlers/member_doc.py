#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os.path
import uuid
import tornado.web
import json
import time
from commons import couch_db


def newTime():
    return time.strftime("%Y-%m-%d", time.localtime())


def docCallBack(file):
    loadDb = couch_db.get(r'/jsmm/%(id)s' % {'id': file['member_id']})
    memberInDb = json.loads(loadDb.body.decode('utf-8'))
    if file['doc_type'] == 'departmentReport':
        memberInDb['departmentReport'] = []
        doc = {
            'depReportTime': newTime(),
            'depReportName': file['filename'],
            'url': file['path']
        }
        memberInDb['departmentReport'].append(doc)
        couch_db.put(r'/jsmm/%(id)s' % {"id": file['member_id']}, memberInDb)
    elif file['doc_type'] == 'departmentInfo':
        memberInDb['departmentInfo'] = []
        doc = {
            'depReportTime': newTime(),
            'depReportName': file['filename'],
            'url': file['path']
        }
        memberInDb['departmentInfo'].append(doc)
        couch_db.put(r'/jsmm/%(id)s' % {"id": file['member_id']}, memberInDb)
    elif file['doc_type'] == 'speechesText':
        memberInDb['speechesText'] = []
        doc = {
            'speechesTextTime': newTime(),
            'speechesTextName': file['filename'],
            'url': file['path']
        }
        memberInDb['speechesText'].append(doc)
        couch_db.put(r'/jsmm/%(id)s' % {"id": file['member_id']}, memberInDb)


class UploadDoc(tornado.web.RequestHandler):

    def initialize(self, callback):
        self._callback = callback

    @tornado.web.addslash
    def post(self):
        """
        接收多个上传文件，调用callback对上传的。
        :return:
        """
        # 文件的保存路径
        inbox_path = os.path.join(os.path.dirname(__file__), '../../inbox/documents')
        # 结构为：{'members': [{'filename': 'xxx.xls', 'body': b'...',
        # 'content_type': 'application/vnd.ms-excel'}]}
        file_infos = self.request.files['doc']
        member_id = self.get_argument('doc_id')
        doc_type = self.get_argument('doc_type')
        for file_info in file_infos:
            filename = file_info['filename']
            upload_path = os.path.join(inbox_path, filename)
            # 在保存的文件名和扩展名中间加6个随机字符，避免文件重名。
            (root, ext) = os.path.splitext(upload_path)
            path = root + '-' + uuid.uuid4().hex[0:6] + ext
            with open(path, 'wb') as file:
                file.write(file_info['body'])
            self._callback({'filename': filename, 'path': path,
                            'content_type': file_info['content_type'],
                            'member_id': member_id, 'doc_type': doc_type})



