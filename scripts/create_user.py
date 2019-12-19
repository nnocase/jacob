# -*- coding: utf-8 -*-
"""
Description: 创建初始用户
Date: 2019-12-13
Author: xgf
"""
import sys

from flask_script import Command
from werkzeug.security import generate_password_hash

from models.base import db
from models.users.users import Admin


class CreatedUser(Command):
    """创建初始用户"""
    def run(self):
        username = 'aon'
        password = '123456'
        password_hash = generate_password_hash(password)

        user = Admin(username=username, password_hash=password_hash, blog_title='', blog_sub_title='',
                     name='aon', about='')

        db.session.add(user)
        db.session.commit()

        print('添加成功')
