# -*- coding:utf-8 -*-
"""
Description: 用户相关路由方法测试
Date: 2019-12-09
Author: xgf
"""
import unittest

import ujson as json

from unittests.base import BaseCase


class TestUser(BaseCase):
    """用户蓝图测试类"""

    def setUp(self):
        super(TestUser, self).setUp()
        self.login()

    def test_update_info(self):
        res = self.client.post(
            '/accounts/info',
            data={'nickname': 'kira', 'avatar': 'img/111.img'}
        ).data
        self.assertEqual(json.loads(res)['code'], 0)

    def test_query_info(self):
        res = self.client.get(
            '/accounts/info',
        ).data
        self.assertEqual(json.loads(res)['code'], 0)

    def test_user_center(self):
        res = self.client.get(
            '/accounts/user_center'
        ).data
        self.assertEqual(json.loads(res)['code'], 0)

    def tearDown(self):
        self.logout()


if __name__ == '__main__':
    unittest.main()
