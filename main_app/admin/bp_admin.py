# -*- coding: utf-8 -*-
"""
Description: 后台
Date: 2019-12-13
Author: xgf
"""
import traceback
import ujson as json

from flask import Blueprint, render_template, redirect, url_for, flash
from flask.views import MethodView
from flask_login import login_required
from werkzeug.security import generate_password_hash

from lib._flask import request_args, request_form
from lib.utils import markdown2html
from models.base import db
from models.posts.posts import Categorys, Posts
from models.users.users import Admin

bp = Blueprint('bp_admin', __name__)


class User(MethodView):
    """后台信息"""
    @login_required
    def get(self):
        admin = Admin.query.order_by(Admin.id.desc()).all()
        items = [a.to_admin() for a in admin]

        return render_template('admin/user.html', items=items, nav='user')


class UserAdd(MethodView):
    """用户添加"""
    @login_required
    def get(self):
        
        return render_template('admin/user_add.html')

    @login_required
    def post(self):
        username = request_form('username', type=str, required=True)
        password = request_form('password', type=str, required=True)
        blog_title = request_form('blog_title', type=str, required=True)
        blog_sub_title = request_form('blog_sub_title', type=str, required=True)
        name = request_form('name', type=str, required=True)
        about = request_form('about', type=str, required=True)

        password_hash = generate_password_hash(password)
        admin = Admin(username=username, password_hash=password_hash, blog_title=blog_title,
                      blog_sub_title=blog_sub_title, name=name, about=about)
        
        try:
            db.session.add(admin)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(traceback.format_exc())
            flash(u'添加失败', 'danger')
            return redirect(url_for('bp_admin.user'))

        flash(u'添加成功', 'success')
        return redirect(url_for('bp_admin.user'))


class UserEdit(MethodView):
    """用户编辑"""
    @login_required
    def get(self):
        id = request_args('id', type=int, required=True)

        admin = Admin.query.get(id)
        if admin is None:
            flash(u'用户不存在', 'danger')
            return redirect(url_for('bp_admin.user'))
        
        item = admin.to_detail()
        return render_template('admin/user_edit.html', item=item)

    @login_required
    def post(self):
        id = request_form('id', type=int, required=True)
        username = request_form('username', type=str, required=True)
        password = request_form('password', type=str, required=True)
        blog_title = request_form('blog_title', type=str, required=True)
        blog_sub_title = request_form('blog_sub_title', type=str, required=True)
        name = request_form('name', type=str, required=True)
        about = request_form('about', type=str, required=True)
        
        password_hash = generate_password_hash(password)
        admin = Admin.query.get(id)
        admin.username = username
        admin.password = password_hash
        admin.blog_title = blog_title
        admin.blog_sub_title = blog_sub_title
        admin.name = name
        admin.about = about

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(u'编辑失败', 'danger')
            return redirect(url_for('bp_admin.user'))

        flash(u'编辑成功', 'success')
        return redirect(url_for('bp_admin.user'))


class UserDel(MethodView):
    """用户删除"""
    @login_required
    def post(self):
        id = request_form('id', type=int, required=True)
        status = request_form('status', type=int, required=True)

        user = Admin.query.get(id)
        if user is None:
            flash(u'用户不存在', 'danger')
            return redirect(url_for('bp_admin.user'))

        user.is_use = status
        try:
            db.session.commit()
        except Exception as e:
            return json.dumps({'code': 1000, 'message': '失败'})
        
        return json.dumps({'code': 1001, 'message': '成功'})

        
class CategoryList(MethodView):
    """分类列表"""
    @login_required
    def get(self):
        cate = Categorys.query.order_by(Categorys.id.desc()).all()
        items = [c.to_admin() for c in cate]

        return render_template('admin/category.html', nav='category', items=items)


class CategoryAdd(MethodView):
    """分类添加"""
    @login_required
    def get(self):

        return render_template('admin/category_add.html')

    @login_required
    def post(self):
        name = request_form('name', type=str, required=True)
        cate = Categorys(name=name)
        try:
            db.session.add(cate)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(traceback.format_exc())
            flash(u'添加失败', 'danger')
            return redirect(url_for('bp_admin.category_list'))

        flash(u'添加成功', 'success')
        return redirect(url_for('bp_admin.category_list'))


class CategoryEdit(MethodView):
    """分类编辑"""
    @login_required
    def get(self):
        id = request_args('id', type=int, required=True)
        cate = Categorys.query.get(id)
        if cate is None:
            flash(u'分类不存在', 'danger')
            return redirect(url_for('bp_admin.category_list'))

        item = cate.to_admin()

        return render_template('admin/category_edit.html', item=item)

    @login_required
    def post(self):
        id = request_form('id', type=int, required=True)
        name = request_form('name', type=str, required=True)

        cate = Categorys.query.get(id)
        cate.name = name
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(traceback.format_exc())
            flash(u'编辑失败', 'danger')
            return redirect(url_for('bp_admin.category_list'))

        flash(u'编辑成功', 'success')
        return redirect(url_for('bp_admin.category_list'))


class CategoryDel(MethodView):
    """分类删除"""
    @login_required
    def post(self):
        id = request_form('id', type=int, required=True)
        status = request_form('status', type=int, required=True)

        user = Categorys.query.get(id)
        if user is None:
            flash(u'分类不存在', 'danger')
            return redirect(url_for('bp_admin.category'))

        ret = user.delete(status)

        return ret


class PostList(MethodView):
    """文章列表"""
    @login_required
    def get(self):
        post = Posts.query.order_by(Posts.id.desc()).all()
        items = [p.to_admin() for p in post]

        return render_template('admin/post.html', nav='post', items=items)


class PostDel(MethodView):
    """文章删除"""
    @login_required
    def post(self):
        id = request_form('id', type=int, required=True)
        status = request_form('status', type=int, required=True)

        post = Posts.query.get(id)
        if post is None:
            flash(u'文章不存在', 'danger')
            return redirect(url_for('bp_admin.post'))

        post.is_use = status
        try:
            db.session.commit()
        except Exception as e:
            return json.dumps({'code': 1000, 'message': '失败'})
        
        return json.dumps({'code': 1001, 'message': '成功'})


# 用户
bp.add_url_rule('/', view_func=User.as_view('user'))
bp.add_url_rule('/add', view_func=UserAdd.as_view('user_add'))
bp.add_url_rule('/edit', view_func=UserEdit.as_view('user_edit'))
bp.add_url_rule('/del', view_func=UserDel.as_view('user_del'))

# 分类
bp.add_url_rule('/category', view_func=CategoryList.as_view('category_list'))
bp.add_url_rule('/category/add', view_func=CategoryAdd.as_view('category_add'))
bp.add_url_rule('/category/edit', view_func=CategoryEdit.as_view('category_edit'))
bp.add_url_rule('/category/del', view_func=CategoryDel.as_view('category_del'))

# 文章
bp.add_url_rule('/post', view_func=PostList.as_view('post'))
bp.add_url_rule('/post/del', view_func=PostDel.as_view('post_del'))
