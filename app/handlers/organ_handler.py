#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json

import tornado.web
import tornado_utils

from commons import couch_db, make_uuid


@tornado_utils.bind_to(r'/organ/?')
class OrganHandler(tornado.web.RequestHandler):
    """组织机构处理类

    URL: '/organ
    """

    def get(self):
        """获取组织机构信息
        """
        response = couch_db.get(r'/jsmm/_design/organ/_view/getOrgan')
        organContent = json.loads(response.body.decode('utf-8'))
        organRow = organContent['rows'][0]
        organValue = organRow['value']
        organ = organValue['organ']

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(organ))


@tornado_utils.bind_to(r'/organ/update/(.+)/(.+)')
class OrganUpdateHandler(tornado.web.RequestHandler):
    def put(self, organId, newOrganValue):
        """修改支社
        """
        response = couch_db.get(r'/jsmm/_design/organ/_view/getOrgan')
        organContent = json.loads(response.body.decode('utf-8'))
        organRow = organContent['rows'][0]
        organValue = organRow['value']

        selector = {"selector": {"branch": {"$eq": organId}}}
        responseMember = couch_db.post(r'/jsmm/_find', selector)
        members = json.loads(responseMember.body.decode('utf-8'))['docs']
        if len(members) < 1:
            pass
        else:
            for member in members:
                member['branch'] = newOrganValue
                couch_db.put(r'/jsmm/%(id)s' % {"id": member['_id']}, member)

        for organ in ((((organValue['organ'])[0])['children'])[0])['children']:
            if organ['id'] == organId:
                organ['text'] = newOrganValue
                organ['id'] = newOrganValue
        couch_db.put(r'/jsmm/%(id)s' % {"id": organValue['_id']}, organValue)
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(organValue['organ']))


@tornado_utils.bind_to(r'/organ/merge/(.+)/(.+)')
class OrganMergeHandler(tornado.web.RequestHandler):
    def put(self, sourcOrganId, targetOrganId):
        '''
        合并支社
        '''
        response = couch_db.get(r'/jsmm/_design/organ/_view/getOrgan')
        organContent = json.loads(response.body.decode('utf-8'))
        organRow = organContent['rows'][0]
        organValue = organRow['value']

        selector = {"selector": {"branch": {"$eq": sourcOrganId}}}
        responseMember = couch_db.post(r'/jsmm/_find', selector)
        members = json.loads(responseMember.body.decode('utf-8'))['docs']
        if len(members) < 1:
            pass
        else:
            for member in members:
                member['branch'] = targetOrganId
                couch_db.put(r'/jsmm/%(id)s' % {"id": member['_id']}, member)

        for organ in ((((organValue['organ'])[0])['children'])[0])['children']:
            if organ['id'] == sourcOrganId:
                ((((organValue['organ'])[0])['children'])[0])['children'].remove(organ)

        couch_db.put(r'/jsmm/%(id)s' % {"id": organValue['_id']}, organValue)

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(organValue['organ']))


@tornado_utils.bind_to(r'/organ/(.+)')
class OrganOperationHandler(tornado.web.RequestHandler):
    def put(self, newOrganValue):
        """新建支社
        """
        response = couch_db.get(r'/jsmm/_design/organ/_view/getOrgan')
        organContent = json.loads(response.body.decode('utf-8'))
        organRow = organContent['rows'][0]
        organValue = organRow['value']

        organ = {};
        organ['id'] = newOrganValue
        organ['text'] = newOrganValue

        if 'children' not in (((organValue['organ'])[0])['children'])[0]:
            ((((organValue['organ'])[0])['children'])[0])['children'] = list()

        ((((organValue['organ'])[0])['children'])[0])['children'].append(organ)

        couch_db.put(r'/jsmm/%(id)s' % {"id": organValue['_id']}, organValue)

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(organValue['organ']))

    def delete(self, organId):
        """删除支社
        """
        response = couch_db.get(r'/jsmm/_design/organ/_view/getOrgan')
        organContent = json.loads(response.body.decode('utf-8'))
        organRow = organContent['rows'][0]
        organValue = organRow['value']

        selector = {"selector": {"branch": {"$eq": organId}}}
        responseMember = couch_db.post(r'/jsmm/_find', selector)
        members = json.loads(responseMember.body.decode('utf-8'))['docs']
        if len(members) < 1:
            pass
        else:
            for member in members:
                member['branch'] = ''
                couch_db.put(r'/jsmm/%(id)s' % {"id": member['_id']}, member)

        for organ in ((((organValue['organ'])[0])['children'])[0])['children']:
            if organ['id'] == organId:
                ((((organValue['organ'])[0])['children'])[0])['children'].remove(organ)

        couch_db.put(r'/jsmm/%(id)s' % {"id": organValue['_id']}, organValue)

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(organValue['organ']))
