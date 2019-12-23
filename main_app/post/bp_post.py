# -*- coding: utf-8 -*-
"""
Description: 文章模块
Date: 2019-12-13
Author: xgf
"""
import datetime
import traceback
import ujson as json

from flask import Blueprint, render_template, url_for, redirect, flash
from flask.views import MethodView
from flask_login import login_required

from lib._flask import request_form, request_args
from lib import utils
from models.base import db
from models.posts.posts import Categorys, Posts

bp = Blueprint('bp_post', __name__)


class Detail(MethodView):
    """文章详情"""
    def get(self):
        id = request_args('id', type=int, required=True)
        post = Posts.query.get(id)

        if post is None:
            return redirect(url_for('bp_home.home'))

        item = post.to_detail()
        return render_template('post/post.html', item=item)


class Add(MethodView):
    """文章添加"""
    @login_required
    def get(self):
        cate = Categorys.query.filter_by(is_use=True).all()
        items = [c.to_admin() for c in cate]

        return render_template('post/add.html', items=items)

    @login_required
    def post(self):
        category_id = request_form('category_id', type=int, required=True)
        title = request_form('title', type=str, required=True)
        body = request_form('body', type=str, required=True)

        post = Posts(title=title, category_id=category_id, body=body)
        try:
            db.session.add(post)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(traceback.format_exc())
            flash(u'添加失败', 'danger')

            return redirect(url_for('bp_admin.post'))

        flash(u'添加失败', 'info')

        return redirect(url_for('bp_admin.post'))


class Edit(MethodView):
    """文章编辑"""
    @login_required
    def get(self):
        id = request_args('id', type=int, required=True)
        inlet = request_args('inlet', type=int, chioces=(1, 2))  # 入口，1: 前台 2: 管理后台
        post = Posts.query.get(id)

        if post is None:
            if inlet == 1:
                flash(u'该文章不存在', 'danger')
                return redirect(url_for('bp_home.home'))
            elif inlet == 2:
                flash(u'该文章不存在', 'danger')
                return redirect(url_for('bp_admin.post'))

        cate = Categorys.query.filter_by(is_use=True).all()
        cate_items = [c.to_admin() for c in cate]
        item = post.to_admin()

        return render_template('post/edit.html', item=item, cate_items=cate_items, inlet=inlet)

    @login_required
    def post(self):
        id = request_form('id', type=int, required=True)
        inlet = request_form('inlet', type=int, chioces=(1, 2))
        category_id = request_form('category_id', type=int, required=True)
        title = request_form('title', type=str, required=True)
        body = request_form('body', type=str, required=True)

        post = Posts.query.get(id)
        post.category_id = category_id
        post.title = title
        post.body = body
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(traceback.format_exc())
            flash(u'编辑失败', 'danger')
            if inlet == 1:
                return redirect(url_for('bp_post.detail', id=id))
            elif inlet == 2:
                return redirect(url_for('bp_admin.post'))

        flash(u'编辑成功', 'danger')
        if inlet == 1:
            return redirect(url_for('bp_post.detail', id=id))
        elif inlet == 2:
            return redirect(url_for('bp_admin.post'))


bp.add_url_rule('/detail', view_func=Detail.as_view('detail'))
bp.add_url_rule('/add', view_func=Add.as_view('add'))
bp.add_url_rule('/edit', view_func=Edit.as_view('edit'))
