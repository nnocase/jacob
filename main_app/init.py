# -*- coding: utf-8 -*-
"""
Description: 配置信息
Date: 2019-12-09
Author: xgf
"""
import os

from flask import Flask, render_template
from redis import Redis
from flaskext.markdown import Markdown

from models import base
from services.accounts import auth


def create_app(config=None):
    """创建app"""
    app = Flask(__name__)
    config = config or 'config.Config'
    app.config.from_object(config)
    
    Markdown(app)
    register_blueprints(app)
    register_error_handler(app)
    register_db(app)
    register_auth(app)
    register_redis(app)
    configure_session(app)
    
    return app


def register_blueprints(app):
    """添加和注册蓝图"""
    from main_app.home import bp_home
    from main_app.auth import bp_auth
    from main_app.post import bp_post
    from main_app.about import bp_about
    from main_app.contact import bp_contact
    from main_app.link import bp_link
    from main_app.admin import bp_admin

    app.register_blueprint(bp_home.bp, url_prefix='/')  # 首页
    app.register_blueprint(bp_auth.bp, url_prefix='/auth')  # 登录模块
    app.register_blueprint(bp_post.bp, url_prefix='/post')  # 文章模块
    app.register_blueprint(bp_about.bp, url_prefix='/about')  # 关于
    app.register_blueprint(bp_contact.bp, url_prefix='/contact')  # 留言
    app.register_blueprint(bp_link.bp, url_prefix='/link')  # 友链
    app.register_blueprint(bp_admin.bp, url_prefix='/admin')  # 管理后台


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
