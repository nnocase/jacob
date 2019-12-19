# -*- encoding:utf-8 -*- 
"""
Description: 例子
Author: xgf
Date: 2019-12-09
"""
from flask_script import Command

from models.base import db


class Example(Command):
    """例子"""
    def run(self):
        print("成功执行example")
