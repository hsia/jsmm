#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os.path
import uuid
import tornado.web
import json
from commons import couch_db


def imageCallBack(file):
    loadDb = couch_db.get(r'/jsmm/%(id)s' % {'id': str(file['member_id'], encoding="utf-8")})
    memberInDb = json.loads(loadDb.body.decode('utf-8'))
    memberInDb['picture'] = '/image/'+file['filename']
    couch_db.put(r'/jsmm/%(id)s' % {"id": str(file['member_id'], encoding="utf-8")}, memberInDb)


class UploadImage(tornado.web.RequestHandler):

    def initialize(self, callback):
        self._callback = callback

    @tornado.web.addslash
    def post(self):
        """
        接收多个上传文件，调用callback对上传的。
        :return:
        """
        # 文件的保存路径
        inbox_path = os.path.join(os.path.dirname(__file__), '../../www/image')
        # 结构为：{'members': [{'filename': 'xxx.xls', 'body': b'...',
        # 'content_type': 'application/vnd.ms-excel'}]}
        file_infos = self.request.files['picture']
        member_id = self.request.arguments['picture_id'][0]

        for file_info in file_infos:
            filename = file_info['filename']
            upload_path = os.path.join(inbox_path)
            # 在保存的文件名和扩展名中间加6个随机字符，避免文件重名。
            # (root, ext) = os.path.splitext(upload_path)
            (name, ext) = os.path.splitext(filename)
            file_name = name + '-' + uuid.uuid4().hex[0:6] + ext
            path = upload_path + '/' + file_name
            with open(path, 'wb') as file:
                file.write(file_info['body'])
            self._callback({'filename': file_name, 'path': path, 'content_type': file_info['content_type'], 'member_id': member_id})
            response = {"fileName": file_name}
            self.write(response)



