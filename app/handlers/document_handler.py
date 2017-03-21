#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json

import tornado.web
import tornado_utils

from commons import couch_db


@tornado_utils.bind_to(r'/document/([0-9a-f]+)')
class DocumentHandler(tornado.web.RequestHandler):
    """文档处理类

    URL: '/document/<document_id>
    """

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
        responseDocument = couch_db.get(r'/jsmm/%(document_id)s' % {"document_id": document_id})
        document = json.loads(responseDocument.body.decode('utf-8'))

        responseMember = couch_db.get(r'/jsmm/%(member_id)s' % {"member_id": document["memberId"]})
        member = json.loads(responseMember.body.decode('utf-8'))
        if document['docType'] == 'researchReport':
            member['researchReport'].remove(document['_id'])
        elif document['docType'] == 'unitedTheory':
            member['unitedTheory'].remove(document['_id'])
        elif document['docType'] == 'politicsInfo':
            member['politicsInfo'].remove(document['_id'])
        elif document['docType'] == 'propaganda':
            member['propaganda'].remove(document['_id'])
        # 删除Document记录
        responseDelDocument = couch_db.delete(r'/jsmm/%(document_id)s?rev=%(document_rev)s' %
                                              {'document_id': document_id, 'document_rev': document['_rev']})
        # 更新member中的document的id
        responseUpdateMember = couch_db.put(r'/jsmm/%(id)s' % {"id": member["_id"]}, member)

        delResult = json.loads(responseDelDocument.body.decode('utf-8'))

        self.write({'success': 'true'})
