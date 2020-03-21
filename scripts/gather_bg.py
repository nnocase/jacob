# -*- coding: utf-8 -*-
"""
Description: 收集背景图
Date: 2020-01-13
Author: xgf
"""
from flask_script import Command

from models.base import db
from models.users.users import Images
from lib._qiniu import upload_by_url


class GatherBG(Command):
    """收集背景图"""
    def run(self):
        for i in range(1, 99):
            url = "https://meiriyiwen.com/images/new_feed/bg_{}.jpg".format(i)
            filename = upload_by_url(url)
            img = Images(name=filename)
            try:
                db.session.add(img)
                db.session.commit()
            except Exception as e:
                print('存入失败')
                db.session.rollback()

            print('存入%d张' % i)

        print('完成')


class BingBG(Command):
    """Bing背景图"""
    def run(self):
        url = "https://api.meowv.com/common/bing"
        filename = upload_by_url(url)
        img = Images(name=filename)
        try:
            db.session.add(img)
            db.session.commit()
        except Exception as e:
            print('存入bing失败')
            db.session.rollback()

        print('存入bing成功')


