# -*- coding: utf-8 -*-
"""
Description: 工具接口
Date: 2019-12-25
Author: xgf
"""
import os
import random
import time
import traceback

import requests
import ujson as json

from flask import Blueprint, current_app, request
from flask.views import MethodView

from lib.utils import create_qrcode
from lib._flask import request_args
from models import Images
from lib._qiniu import upload_file, fill_domain, upload_data

bp = Blueprint('bp_tool', __name__)


@bp.route('/share/wxqrcode')
def wx_arcode():
    """
        生成分享至微信的二维码
        param url
    """
    url = request_args('url', type=str, required=True)
    path = './main_app/static/images/qrcode/{}.png'.format(str(int(time.time()*10000000)) + str(random.randint(0, 9999)))

    ok = create_qrcode(url, path)
    if ok:
        img_url = fill_domain(upload_file(path, path))
        os.remove(path)
        return json.dumps({'code': 1001, 'message': '成功', 'datas': img_url})
    else:
        return json.dumps({'code': 1000, 'message': '失败'})


@bp.route('/random/bg')
def random_bg():
    """
        随机背景图
    """
    images = Images.query.filter_by(is_use=True).all()
    images = [i.to_list() for i in images]
    bg = random.choice(images)['name']

    return json.dumps({'code': 1001, 'message': '成功', 'datas': bg})


class EditorUpload(MethodView):
    """编辑器上传图片"""
    def post(self):
        try:
            image = request.files.get("editormd-image-file", None)
            print(image)
        except Exception as e:
            print(traceback.format_exc())
            return json.dumps({'success': 0, 'message': '上传失败'})

        url = fill_domain(upload_data(image)) if image else ''

        return json.dumps({'success': 1, 'message': '上传成功', 'url': url})


bp.add_url_rule('/editor/upload', view_func=EditorUpload.as_view('editor_upload'))