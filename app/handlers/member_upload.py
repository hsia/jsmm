#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os.path
import uuid

import tornado.web


class UploadHandler(tornado.web.RequestHandler):
    def initialize(self, callback):
        '''
        callback(file_info)，其中file_info格式为：
        {'filename': 'xxx.xls', 'path': 'aaa/bbb/xxx.xls', 'content_type': 'application/vnd.ms-excel'}
        filename为原文件名，path为实际保存路径，content_type为文件类型
        '''
        self._callback = callback

    @tornado.web.addslash
    def get(self):
        self.write('''
<html>
  <head><title>Upload File</title></head>
  <body>
    <form action='/members/upload/' enctype="multipart/form-data" method='post'>
    <input type='file' name='members'/><br/>
    <input type='submit' value='submit'/>
    </form>
  </body>
</html>
''')

    @tornado.web.addslash
    def post(self):
        """
        接收多个上传文件，调用callback对上传的。
        :return:
        """
        # 文件的保存路径
        inbox_path = os.path.join(os.path.dirname(__file__), '../../inbox/members')
        # 结构为：{'members': [{'filename': 'xxx.xls', 'body': b'...',
        # 'content_type': 'application/vnd.ms-excel'}]}
        file_infos = self.request.files['members']

        error_message = []
        for file_info in file_infos:
            filename = file_info['filename']
            upload_path = os.path.join(inbox_path, filename)
            # 在保存的文件名和扩展名中间加6个随机字符，避免文件重名。
            (root, ext) = os.path.splitext(upload_path)
            path = root + '-' + uuid.uuid4().hex[0:6] + ext
            with open(path, 'wb') as file:
                file.write(file_info['body'])
            msgs = self._callback({'filename': filename, 'path': path, 'content_type': file_info['content_type']})
            # if not msgs['success'] and msgs.get('filename', False):
            #     error_message.append({'filename': msgs['filename']})
            # elif not msgs['success'] and msgs.get('name', False):
            #     error_message.append({"name": msgs["name"], "birthday": msgs["birthday"]})

            if not msgs['success']:
                error_message.append({"fileName": msgs["fileName"], "errorContent": msgs["errorContent"]})

        if len(error_message):
            self.write({"success": False, "msg": error_message})
        else:
            self.write({"success": True, "msg": error_message})
