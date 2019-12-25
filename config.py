# -*- coding: utf-8 -*- 
""" 
Description: 总体配置 
Date: 2019-12-09 
Author: xgf 
""" 
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config(object):
    """生产配置信息"""
    PORT = 16211
    BABEL_DEFAULT_LOCALE = 'zh_CN'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TOKEN_TIME = 60 * 60 * 12
    DEBUG = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_DATABASE_URI = os.environ.get('PSQL_URI')  # 数据库连接地址

    SUBSYS_ROUTER_HOST = 'http://127.0.0.1'

    REDIS_CONFIG = {
        "HOST": "127.0.0.1", 
        "PORT": 6379,
        "PASS": "",
        "DB": 0,
        "CELERY_DB": 12,
    }

    CELERY_BROKEY = "redis://:{}@{}:{}/{}".format(REDIS_CONFIG['PASS'], REDIS_CONFIG['HOST'],
                                            REDIS_CONFIG['PORT'], REDIS_CONFIG['CELERY_DB'])

    DOMAIN = 'http://www.icenglou.cn'
    OPERATION_LOG = os.environ.get('OPERATION_LOG')


class DevConfig(Config):
    """开发环境配置信息"""
    PORT = 5000
    DEBUG = True
    SECRET_KEY = os.environ.get('DEV_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('PSQL_URI')

    SUBSYS_ROUTER_HOST = 'http://127.0.0.1'

    DOMAIN = 'example.com'
    OPERATION_LOG = os.environ.get('DEV_OPERATIOON_LOG')

