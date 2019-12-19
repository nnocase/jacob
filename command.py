# -*- coding: utf-8 -*-
"""
Description: 命令
Date: 2019-12-09
Author: xgf
"""
from flask_script import Manager

from wsgi import app

manager = Manager(app)

# 导入要执行的脚本
from scripts import example
from scripts import create_user

manager.add_command('example', example.Example())
manager.add_command('create_user', create_user.CreatedUser())


if __name__ == '__main__':
    manager.run()
