# -*- encoding: utf-8 -*-
"""
Desciption: 工具包🔧
Author: xgf
Date: 2019-12-09
"""
import datetime
import hashlib
from random import choice
import re
import os

import qrcode
import markdown
import requests


def md5(_str):
    return hashlib.md5(_str).hexdigest()

def sha1(_str):
    _str = _str.encode("utf-8")
    return hashlib.sha1(_str).hexdigest()

def time_format(created, pattern="%Y-%m-%d %H:%M:%S"):
    """处理时间格式"""
    _str = datetime.datetime.strftime(created, pattern) if created else ''

    return _str


def markdown2html(text):
    extensions = [
        'fenced_code',
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc'
    ]

    return markdown.markdown(text, extensions=extensions)


def remove_tag(html):
    """去除html标签"""
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', html)

    return dd


def create_qrcode(url, filepath):
    """生成二维码"""
    try:
        qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=1)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image()
        img.save(filepath)
        print("生成二维码完成")
        return True
    except Exception as e:
        print(e)
        return False


def save_img(picurl, filepath):
    """下载图片"""
    try:
        file_suffix = os.path.splitext(picurl)[1]
        if file_suffix:
            file_suffix = file_suffix
        else:
            file_suffix = '.jpg'
        imgdate = requests.get(picurl).read()
        filepath = filepath + file_suffix
        output = open(filepath, 'wb+')
        output.write(imgdate)
        output.close()
        print("下载完成")
    except Exception as e:
        print(e)