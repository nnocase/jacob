# -*- coding: utf-8 -*-
"""
Description: 配置信息
Date: 2019-12-09
Author: xgf
"""
import os
from datetime import datetime

from flask import Flask, render_template, request, current_app, redirect
from flask_login import current_user
from redis import Redis
from flaskext.markdown import Markdown
from bs4 import BeautifulSoup as bs

from models import base
from services.accounts import auth
from lib.flask_logging import enable_logging


def prettify(html):
    """解析html"""
    soup = bs(html, 'html.parser')
    return soup.prettify()


def create_app(config=None):
    """创建app"""
    app = Flask(__name__)
    config = config or 'config.Config'
    app.config.from_object(config)
    
    register_logger(app)
    Markdown(app)
    register_blueprints(app)
    register_error_handler(app)
    register_db(app)
    register_auth(app)
    register_redis(app)
    register_before_request(app)
    configure_session(app)
    # register custom filter in flask app
    app.jinja_env.filters['prettify'] = prettify

    return app


def register_logger(app):
    """日志"""
    if app.debug:
        return
    enable_logging(app)

def register_blueprints(app):
    """添加和注册蓝图"""
    from main_app.home import bp_home
    from main_app.auth import bp_auth
    from main_app.post import bp_post
    from main_app.about import bp_about
    from main_app.contact import bp_contact
    from main_app.link import bp_link
    from main_app.admin import bp_admin
    from main_app.tool import bp_tool
    from main_app.wechat import bp_pub_account

    app.register_blueprint(bp_home.bp, url_prefix='/')  # 首页
    app.register_blueprint(bp_auth.bp, url_prefix='/auth')  # 登录模块
    app.register_blueprint(bp_post.bp, url_prefix='/post')  # 文章模块
    app.register_blueprint(bp_about.bp, url_prefix='/about')  # 关于
    app.register_blueprint(bp_contact.bp, url_prefix='/contact')  # 留言
    app.register_blueprint(bp_link.bp, url_prefix='/link')  # 友链
    app.register_blueprint(bp_admin.bp, url_prefix='/admin')  # 管理后台
    app.register_blueprint(bp_tool.bp, url_prefix='/tool')  # 工具
    app.register_blueprint(bp_pub_account.bp, url_prefix='/wechat/pub/account') # 微信公众号    


def register_db(app):
    """初始化db"""
    base.db.init_app(app)


def register_redis(app):
    cfg = app.config['REDIS_CONFIG']
    redis = Redis(host=cfg['HOST'], port=cfg['PORT'], db=cfg['DB'], password=cfg['PASS'])
    app.redis = redis


def register_auth(app):
    auth.login_manager.init_app(app)
    auth.login_manager.login_view = "bp_auth.login"


def configure_session(app):
    from flask_session import Session
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = app.redis
    app.config['PERMANENT_SESSION_LIFETIME'] = app.config['TOKEN_TIME']
    Session(app)


def register_error_handler(app):
    @app.errorhandler(400)
    def err_400(error):
        return render_template('base/400.html')
    
    @app.errorhandler(403)
    def err_403(error):
        return render_template('base/403.html')

    @app.errorhandler(404)
    def err_404(error):
        return render_template('base/404.html')

    @app.errorhandler(500)
    def err_500(error):
        return render_template('base/500.html')

    @app.errorhandler(502)
    def err_502(error):
        return render_template('base/502.html')

    @app.errorhandler(504)
    def err_504(error):
        return render_template('base/504.html')


def register_before_request(app):
    @app.before_request
    def before_request():
        """请求验证"""
        path = request.path
        if path and path.startswith("/static/"):
            return

        # if not current_user.is_authenticated:
        #     if path != "/auth/login":
        #         return redirect("/auth/login")

        current_user.last_login = datetime.now()
        base.db.session.commit()
        # 操作日志记录文件
        json_form_data = {key: dict(request.form)[key] for key in dict(request.form)}
        json_args_data = {key: dict(request.args)[key] for key in dict(request.args)}
        referer = request.headers.get('Referer')
        x_real_ip = request.headers.get('X-Real-Ip')

        if current_user.is_authenticated:
            _str = str(referer) + ' ' + str(path) + ' ' + str(x_real_ip) + ' ' \
                   + str(current_user.id) + ' ' + str(current_user.name) + ' ' \
                   + str(current_user.username) + ' ' + str(json_args_data) + ' ' + \
                   str(json_form_data) + ' ' + str(datetime.now())
            with open(app.config["OPERATION_LOG"], 'a+') as f:
                f.write(_str + '\n')