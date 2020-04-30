# -*- coding: utf-8 -*-
"""
Description: 微信公众号后台
Date: 202--04-30
Author: xgf
"""
import requests
from flask import request, Blueprint, current_app

from lib._flask import request_args
from lib.utils import sha1

bp = Blueprint('bp_pub_account', __name__)


@bp.route("/index", methods=['POST'])
def index():
    """
        @公众号服务配置
        signature 微信加密签名
        timestamp 时间戳
        nonce 随机数
        echostr 随机字符串
    """
    signature = request_args('signature')
    timestamp = request_args('timestamp')
    nonce = request_args('nonce')
    echostr = request_args('echostr')
    token = '82801be44fc08479560ef80b'  # 配置填写的token

    data = [token, timestamp, nonce]
    data.sort()

    temp = ''.join(data)
    mysignature = sha1(temp)

    # 加密后的字符串可与signature对比，标识该请求来源于微信
    if signature == mysignature:
        return 'success'
    else:
        return 'success'
