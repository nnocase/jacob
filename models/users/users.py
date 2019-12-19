# -*- encoding:utf-8 -*-
"""
Description: 用户模块
Author: xgf
Date: 2019-12-09
"""
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text

from models.base import db
from lib.utils import time_format, markdown2html


class Admin(db.Model, UserMixin):
    """管理后台"""
    __tablename__ = 'admin'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 加密密码
    blog_title = db.Column(db.String(60))  # 网站标题
    blog_sub_title = db.Column(db.String(100))  # 网站子标题
    name = db.Column(db.String(30))  # 名称
    about = db.Column(db.Text)  # 关于
    is_use = db.Column(db.Boolean, default=True)  # 是否显示
    created = db.Column(db.DateTime, default=text('Now()'))  # 创建时间

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_admin(self):
        data = {
            'id': self.id,
            'username': self.username,
            'password': self.password_hash,
            'blog_title': self.blog_title,
            'blog_sub_title': self.blog_sub_title,
            'name': self.name,
            'about': markdown2html(self.about),
            'is_use': self.is_use,
            'created': time_format(self.created)
        }
        
        return data

    def to_detail(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password_hash,
            'blog_title': self.blog_title,
            'blog_sub_title': self.blog_sub_title,
            'name': self.name,
            'about': self.about,
            'is_use': self.is_use,
            'created': time_format(self.created)
        }
