# -*- encoding -*- 
"""
Description: 首页
Author: xgf
Date: 2019-12-11
"""
import os
import time
from lib.utils import md5

from flask import (Blueprint, render_template, current_app, url_for, 
                    send_from_directory, make_response)
from flask.views import MethodView

from lib._flask import request_args
from models.posts.posts import Posts, Categorys
from models.users.users import Admin, Images

bp = Blueprint('bp_home', __name__)


class Home(MethodView):
    """首页"""
    def get(self):
        page = request_args('page', type=int, default=1)
        size = request_args('size', type=int, default=20)
        category_id = request_args('category_id', type=int, default=0)

        category = Categorys.query.filter_by(is_use=True).all()
        cate_items = [c.to_admin() for c in category]

        site = Admin.query.filter_by(is_use=True).first()
        site = site.to_admin()

        query = Posts.query.filter_by(is_use=True).order_by(Posts.id.desc())
        if category_id:
            query = query.filter_by(category_id=category_id)

        count = query.count() or int(1)
        posts = query.limit(size).offset((page-1) * size).all()
        items = [p.to_home() for p in posts]
        endpage = int((count / size) if (count % size == 0) else (count / size + 1))

        return render_template('home/index.html', site=site, items=items, cate_items=cate_items,
                               page=page, endpage=endpage, category_id=category_id)


class Favicon(MethodView):
    def get(self):

        return send_from_directory(os.path.join(current_app.root_path, 'static'),
                            'favicon.ico', mimetype='image/vnd.microsoft.icon')


class Rss(MethodView):
    def get(self):
        page = request_args('page', type=int, default=1)
        size = request_args('size', type=int, default=20)
        site = Admin.query.filter_by(is_use=True).first()
        site = site.to_admin()
        query = Posts.query.filter_by(is_use=True)

        count = query.count() or int(1)
        posts = query.limit(size).offset((page-1) * size).all()
        items = [p.to_home() for p in posts]

        template = render_template('home/cenglou.xml', site=site, items=items)
        response = make_response(template)
        response.headers['Content-Type'] = 'application/rss+xml;charset=utf-8'

        return response


bp.add_url_rule('/', view_func=Home.as_view('home'))
bp.add_url_rule('/favicon.ico', view_func=Favicon.as_view("favicon"))
bp.add_url_rule('/feed', view_func=Rss.as_view("feed"))
