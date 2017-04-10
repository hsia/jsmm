#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import urllib

import tornado.web
import tornado_utils

from commons import couch_db, couchLucene_db


@tornado_utils.bind_to(r'/documents/?')
class DocumentHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        """修改_id为member_id的member对象。
        """
        response = couch_db.get(r'/jsmm/_design/documents/_view/by-memberid')
        doucment_list = json.loads(response.body.decode('utf-8'))
        documents = []
        for row in doucment_list['rows']:
            documents.append(row['value'])
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(documents))

    def post(self):
        """
        修改_id为member_id的member对象。
        """
        params = json.loads(self.request.body.decode('utf-8'))

        page_number = params['page']
        page_size = params['rows']

        sort_by = params.get('order', 'asc')
        if sort_by == 'desc':
            sort_by_result = True
            sort_by_fti = '\/fileUploadTime<date>'
        else:
            sort_by_result = False
            sort_by_fti = '\\fileUploadTime<date>'

        params_str = ""
        if "documentInfo" in params:
            # name = params["documentInfo"]["name"]
            # fileName = params["documentInfo"]["fileName"]
            key_world = params["documentInfo"]["keyWord"].replace(' ', '')
            key_word_attachment = params["documentInfo"]["keyWordAttachment"]
            start_date = params["documentInfo"]["startDate"]
            end_date = params["documentInfo"]["endDate"]
            doc_type = params["documentInfo"]["docType"]

            if key_word_attachment != '':
                params_str += key_word_attachment
            else:
                pass

            # if name != '' and params_str != '':
            #     params_str += ' AND name:"' + name + '"'
            # elif name != '' and params_str == '':
            #     params_str += 'name:"' + name + '"'
            # else:
            #     pass
            #
            # if fileName != '' and params_str != '':
            #     params_str += ' AND fileName:"' + fileName + '"'
            # elif fileName != '' and params_str == '':
            #     params_str += 'fileName:"' + fileName + '"'
            # else:
            #     pass
            if key_world != '' and params_str != '':
                params_str += ' AND (fileName:' + key_world + ' OR name:' + key_world + ')'
            elif key_world != '' and params_str == '':
                params_str += '(fileName:' + key_world + ' OR name:' + key_world + ')'
            else:
                pass

            if start_date != '' and end_date != '' and params_str != '':
                params_str += ' AND fileUploadTime<date>:[' + start_date + ' TO ' + end_date + ']'
            elif start_date != '' and end_date != '' and params_str == '':
                params_str += 'fileUploadTime<date>:[' + start_date + ' TO ' + end_date + ']'
            else:
                pass

            if doc_type != '' and params_str != '':
                params_str += ' AND docType:"' + doc_type + '"'
            elif doc_type != '' and params_str == '':
                params_str += 'docType:"' + doc_type + '"'
            else:
                pass

        if "branch" in params:
            branch = params["branch"]

            if branch != '' and params_str != '' and branch != '北京市' and branch != '朝阳区':
                params_str += ' AND branch:"' + branch + '"'
            elif branch != '' and params_str == '' and branch != '北京市' and branch != '朝阳区':
                params_str += 'branch:"' + branch + '"'
            else:
                pass

        print('params_str = ' + params_str)


        if params_str != '':
            print(
                r'/_fti/local/jsmm/_design/documents/by_doc_info?q=%(params_str)s&limit=%(limit)s&skip=%(skip)s&sort=%(sort_by_fti)s' % {
                    "params_str": urllib.parse.quote(params_str, "utf-8"), 'limit': page_size,
                    'skip': (page_number - 1) * page_size,
                    'sort_by_fti': sort_by_fti})
            response = couchLucene_db.get(
                r'/_fti/local/jsmm/_design/documents/by_doc_info?q=%(params_str)s&limit=%(limit)s&skip=%(skip)s&sort=%(sort_by_fti)s' % {
                    "params_str": urllib.parse.quote(params_str, "utf-8"), 'limit': page_size,
                    'skip': (page_number - 1) * page_size,
                    'sort_by_fti': sort_by_fti})
        else:
            print(
                r'/jsmm/_design/documents/_view/by_memberid?limit=%(page_size)s&skip=%(page_number)s&descending=%(sort_by_result)s' % {
                    'page_size': page_size, 'page_number': (page_number - 1) * page_size,
                    'sort_by_result': sort_by_result})
            response = couch_db.get(
                r'/jsmm/_design/documents/_view/by_memberid?limit=%(page_size)s&skip=%(page_number)s&descending=%(sort_by_result)s' % {
                    'page_size': page_size, 'page_number': (page_number - 1) * page_size,
                    'sort_by_result': sort_by_result})

        documents_result = {}
        if response.code == 200:
            documents = []
            document_list = json.loads(response.body.decode('utf-8'))
            print(document_list)

            if params_str != '':
                for row in document_list['rows']:
                    row['fields']['_id'] = row['id']
                    documents.append(row['fields'])
            else:
                for row in document_list['rows']:
                    documents.append(row['value'])

            documents_result['total'] = document_list['total_rows']
            documents_result['rows'] = documents
        else:
            documents_result['total'] = 0
            documents_result['rows'] = []

        documents_result['page_size'] = page_size
        documents_result['page_number'] = page_number

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(documents_result))
