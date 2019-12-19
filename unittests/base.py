# -*- coding:utf-8 -*-
"""
Description: 单元测试
Date: 2019-12-09
Author: xgf
"""
import unittest
import traceback
import datetime
import urllib

import ujson as json

from wsgi import app


class BaseCase(unittest.TestCase):
    """ 单元测试基类 """
    def setUp(self):
        """ 开始时初始化 """
        self.app = app
        self.client = app.test_client()

    def tearDown(self):
        """ 结束时处理 """
        pass

    def login(self, phone='', password=''):
        """登录"""
        r = self.client.post('/accounts/login', data={'phone': phone, 'password': password},
             follow_redirects=True)
        #print r.data
        r = json.loads(r.data)
        #print r.get('msg')

    def login2(self, phone='', password=''):
        """登录"""
        r = self.client.post('/accounts/login', data={'phone': phone, 'password': password},
             follow_redirects=True)
        #print r.data
        r = json.loads(r.data)
        #print r.get('msg')


    def logout(self):
        self.client.get('/accounts/logout')

    def get(self, url, params={}, headers={}):
        res = self.client.get(url + '?' + urllib.urlencode(params), headers=headers)
        return json.loads(res.data)

    def post(self, url, data={}, headers={}):
        res = self.client.post(url, data=data, headers=headers)
        return json.loads(res.data)
        


if __name__ == '__main__':
    unittest.main()
