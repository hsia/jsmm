#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json

import tornado.web

from commons import couch_db
from lib import tornado_utils


@tornado_utils.bind_to(r'/document/([0-9a-f]+)')
class DocumentHandler(tornado.web.RequestHandler):
    """文档处理类

    URL: '/document/<document_id>
    """

    def data_received(self, chunk):
        pass

    def get(self, document_id):
        """获取文档信息
        """
        self.write(couch_db.get(r'/jsmm/%(document_id)s' %
                                {'document_id': document_id}))

    def put(self, document_id):
        """修改文档信息
        """
        pass

    def delete(self, document_id):
        """删除文档：
            包括删除文档记录和更新memer中的文档id
        """
        response_document = couch_db.get(r'/jsmm/%(document_id)s' % {"document_id": document_id})
        document = json.loads(response_document.body.decode('utf-8'))

        response_member = couch_db.get(r'/jsmm/%(member_id)s' % {"member_id": document["memberId"]})
        member = json.loads(response_member.body.decode('utf-8'))
        if document['docType'] == 'researchReport':
            member['researchReport'].remove(document['_id'])
        elif document['docType'] == 'unitedTheory':
            member['unitedTheory'].remove(document['_id'])
        elif document['docType'] == 'politicsInfo':
            member['politicsInfo'].remove(document['_id'])
        elif document['docType'] == 'propaganda':
            member['propaganda'].remove(document['_id'])
        # 删除Document记录
        couch_db.delete(r'/jsmm/%(document_id)s?rev=%(document_rev)s' %
                        {'document_id': document_id, 'document_rev': document['_rev']})
        # 更新member中的document的id
        couch_db.put(r'/jsmm/%(id)s' % {"id": member["_id"]}, member)

        # del_result = json.loads(response_del_document.body.decode('utf-8'))

        self.write({'success': 'true'})
