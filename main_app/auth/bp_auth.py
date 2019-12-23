# -*- enconding:utf-8 -*-
"""
Description: 登录模块
Author: xgf
Date: 2019-12-11
"""
import datetime

from flask import (Blueprint, render_template, redirect, url_for, session,
                   get_flashed_messages, flash)
from flask.views import MethodView
from flask_login import login_user, logout_user, current_user

from lib._flask import request_form
from models.users.users import Admin
from services.accounts.auth import set_user_online, set_user_offline

bp = Blueprint('bp_auth', __name__)


class Login(MethodView):
    """登录"""
    def get(self):
        if current_user.is_authenticated:
            print(current_user)
            flash(u'已登录，不要重复登录', 'danger')
            return redirect(url_for('bp_admin.user'))

        return render_template('auth/login.html')

    def post(self):
        username = request_form('username', type=str, required=True)
        password = request_form('password', type=str, required=True)

        user = Admin.query.filter_by(username=username).first()
        if user is None:
            return render_template('auth/login.html', user_error=u'账号不存在',
                                   username=username, password=password)

        if user.validate_password(password):
            set_user_offline(user.id)
            login_user(user)
            set_user_online(user.id, session.sid)
            get_flashed_messages()
            return redirect(url_for('bp_admin.user'))
        else:
            return render_template('auth/login.html', pwd_error=u'密码错误',
                                   username=username, password=password)


class Logout(MethodView):
    """退出"""
    def get(self):
        logout_user()

        return redirect(url_for('bp_home.home'))


bp.add_url_rule('/login', view_func=Login.as_view('login'))
bp.add_url_rule('/logout', view_func=Logout.as_view('logout'))
