# -*- encoding: utf-8 -*-
"""
Desciption: 工具包🔧
Author: xgf
Date: 2019-12-09
"""
import datetime
import markdown


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
