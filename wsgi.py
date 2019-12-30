# -*- coding: utf-8 -*-
"""
Description: wsgi
Date: 2019-12-09
Author: xgf
"""
import configparser

from main_app import init

cf = configparser.ConfigParser()
cf.read("deploy/uwsgi.ini")
svrtype = cf.get("server", "type")
if svrtype.lower() == "master":
    print("running with config.config ...")
    app = init.create_app()
    app.is_prod = True
else:
    print("running with config.DevConfig ...")
    app = init.create_app("config.DevConfig")
    app.is_prod = False


if __name__ == '__mian__':
    app.run(port=app.config['PORT'])
