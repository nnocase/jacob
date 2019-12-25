# -*- coding: utf-8 -*-
"""
Description: 工具接口
Date: 2019-12-25
Author: xgf
"""
import time
import ujson as json

from flask import Blueprint, current_app

from lib.utils import create_qrcode
from lib._flask import request_args

bp = Blueprint('bp_tool', __name__)


@bp.route('/share/wxqrcode')
def wx_arcode():
    """
        生成分享至微信的二维码
        param url
    """
    url = request_args('url', type=str, required=True)
    path = './main_app/static/images/qrcode/{}.png'.format(time.time())

    ok = create_qrcode(url, path)
    if ok:
        img_url = current_app.config['SUBSYS_ROUTER_HOST'] + ':' + str(current_app.config['PORT']) + path[10:]
        return json.dumps({'code': 1001, 'message': '成功', 'datas': img_url})
    else:
        return json.dumps({'code': 1000, 'message': '失败'})
