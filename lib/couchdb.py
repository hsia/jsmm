#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Copyright sunhaitao@devTaste.com
'''
import json

from tornado.httpclient import HTTPClient, HTTPError, HTTPRequest


class CouchDB(object):
    """
    封装访问CouchDB的GET、HEAD、PUT、POST、DELETE方法。
    """
    def __init__(self, base_uri):
        self.__base_uri = base_uri

    def __fetch(self, method, path, content_type=None, data=None):
        assert path[0] == '/'
        headers = {}
        body = None
        if method == 'PUT' or method == 'POST':
            if content_type is None:
                headers['Content-Type'] = 'application/json'
                if data is None:
                    body = ''
                else:
                    str(data)
                    body = json.dumps(data)
            else:
                headers['Content-Type'] = content_type
                body = data
        request = HTTPRequest(
            self.__base_uri + path,
            method,
            headers=headers,
            body=body
        )
        http_client = HTTPClient()
        try:
            return http_client.fetch(request)
        except HTTPError as error:
            return error
        finally:
            http_client.close()

    def get(self, path):
        """
        GET方法。
        """
        return self.__fetch('GET', path)

    def head(self, path):
        """
        HEAD方法。
        """
        return self.__fetch('HEAD', path)

    def put(self, path, data=None, content_type=None):
        """
        PUT方法。
        """
        return self.__fetch(
            'PUT',
            path,
            content_type=content_type,
            data=data
        )

    def post(self, path, data=None, content_type=None):
        """
        POST方法。
        """
        return self.__fetch(
            'POST',
            path,
            content_type=content_type,
            data=data
        )

    def delete(self, path):
        """
        DELETE方法。
        """
        return self.__fetch('DELETE', path)
