# -*- coding: utf-8 -*-
"""
Description: 登录验证
Date: 2019-12-13
Author: xgf
"""
from flask import current_app
from flask_login import LoginManager
from models.users.users import Admin

login_manager = LoginManager()
USER_LOGIN_KEY_PREFIX='user-login'
SESSION_KEY_PREFIX='session:'


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


def set_user_online(user_id, session_id):
    user_key = USER_LOGIN_KEY_PREFIX + str(user_id)
    value = SESSION_KEY_PREFIX + str(session_id)
    current_app.redis.setex(name=user_key, value=session_id, time=current_app.config['TOKEN_TIME'])


def get_user_session_id(user_id):
    session_id = current_app.redis.get(USER_LOGIN_KEY_PREFIX + str(user_id))
    return session_id


def set_user_offline(user_id):
    try:
        session_id = get_user_session_id(user_id).decode()
        if session_id is None:
            return

        current_app.redis.delete(SESSION_KEY_PREFIX + session_id)
        current_app.redis.delete(USER_LOGIN_KEY_PREFIX + str(user_id))

    except Exception as e:
        print(e, "error set_user_offline")
