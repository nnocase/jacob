# -*- encoding:utf-8 -*-
"""
Description: 文章模块
Author: xgf
Date: 2019-12-09
"""
import datetime
import ujson as json 

from sqlalchemy import text

from ..base import db
from lib.utils import time_format,markdown2html


class Categorys(db.Model):
    """文章分类"""
    __tablename__ = 'categorys'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)  # 名称
    is_use = db.Column(db.Boolean, default=True)  # 是否使用
    created = db.Column(db.DateTime, server_default=text('Now()'))  # 创建时间

    def delete(self, status):
        default_category = Categorys.query.get(1)
        posts = Posts.query.filter_by(category_id=self.id).all()
        for post in posts:
            post.is_use = status

        self.is_use = status
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return json.dumps({'code': 1000, 'message': '失败'})

        return json.dumps({'code': 1001, 'message': '成功'})

    
    def to_admin(self):
        return {
            'id': self.id,
            'name': self.name,
            'is_use': self.is_use,
            'created': time_format(self.created)
        }
        

class Posts(db.Model):
    """文章"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))  # 标题
    body = db.Column(db.Text)  # 主题
    created = db.Column(db.DateTime, server_default=text('Now()'), index=True)  # 创建时间
    can_comment = db.Column(db.Boolean, default=True)  # 能否评论
    is_use = db.Column(db.Boolean, default=True)  # 是否使用
    category_id = db.Column(db.Integer)

    def delete(self):
        self.is_use = False
        db.session.commit()
    
    def to_home(self):
        cate = Categorys.query.get(self.category_id)
        category_name = cate.name if cate else ''

        return {
            'id': self.id,
            'category_id': self.category_id,
            'category_name': category_name,
            'title': self.title,
            'body': markdown2html(self.body),
            'can_comment': self.can_comment,
            'is_use': self.is_use,
            'created': time_format(self.created)
        }

    def to_detail(self):
        return self.to_home()

    def to_admin(self):
        post = self.to_home()
        post['body'] = self.body

        return post


class Comments(db.Model):
    """评论"""
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))  # 评论者姓名
    email = db.Column(db.String(254))  # 邮箱
    site = db.Column(db.String(255))  # 网站
    body = db.Column(db.Text)  # 评论主体
    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    is_use = db.Column(db.Boolean, default=True)  # 是否使用
    created = db.Column(db.DateTime, server_default=text('Now()'), index=True)  # 创建时间

    replied_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)
    
    def delete(self):
        self.is_use = False
        db.session.commit()


class Links(db.Model):
    """链接"""
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))  # 名称
    url = db.Column(db.String(255))  # url
    is_use = db.Column(db.Boolean, default=True)  # 是否使用
    created = db.Column(db.DateTime, server_default=text('Now()'))  # 创建时间

    def delete(self):
        self.is_use = False
        db.session.commit()


