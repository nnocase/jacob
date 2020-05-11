# -*- coding: utf-8 -*-
"""
Description: 七牛上传文件工具
Date: 2020-01-13
Author: xgf
"""
import random
import time

import requests
from flask import current_app
from qiniu import Auth, put_data, put_file

from lib.utils import md5

ALLOWED_EXTENSIONS = set(['png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG', 'gif', 'GIF'])

def upload_qiniu(filename, data, mode, bucket_name='xgf', config=None):
    """上传到七牛"""
    if not config:
        config = current_app.config

    cgf = config['QINIU_SETTINGS']
    access_key = cgf['access_key']
    secret_key = cgf['secret_key']

    auth = Auth(access_key, secret_key)
    token = auth.upload_token(bucket_name, filename)

    if mode == 'data':
        # 以二进制流方式上传
        ret, info = put_data(token, filename, data)
    elif mode == 'file':
        # 以文件方式上传
        ret, inof = put_file(token, filename, data)

    assert ret["key"] == filename

    return filename


def get_filename(filename):
    """文件随机重命名"""
    filetype = filename.split('.')[-1] if '.' in filename else ''
    prefix = str(int(time.time()*10000000)) + str(random.randint(0, 9999))

    return '%s.%s' % (prefix, filetype)


def upload_data(file):
    """以二进制流方式上传本地文件"""
    data = file.read()
    filename = get_filename(file.filename)

    return upload_qiniu(filename, data, mode='data')


def upload_file(filename, filepath):
    """以文件方式上传本地文件"""
    filename = get_filename(filename)

    return upload_qiniu(filename, filepath, mode='file')


def upload_by_url(url):
    """通过url上传网络文件"""
    data = requests.get(url, timeout=(3, 7)).content

    filename = md5(data)  # 使用md5

    return upload_qiniu(filename, data, mode='data')


def fill_domain(filename, http=False):
    """
    文件名称填充域名信息，组成完整的链接。
    param: filename: 文件名称
    param: http: 是否是http协议，否的话采用https协议
    """
    if not filename.startswith('http'):
        if http:
            filename = 'http://%s/%s' % (current_app.config['QINIU_IMG_HOST'], filename)
        else:
            filename = 'https://%s/%s' % (current_app.config['QINIU_IMG_HOST'], filename)
    return filename



