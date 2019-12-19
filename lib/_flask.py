# -*- enconding -*- 
"""
Description: 请求工具(封装flask的请求工具)
Author: xgf
Dete: 2019-12-10
"""
from functools import wraps, partial
from flask import abort, current_app, request


def get_param(key, default=None, type=None, required=False, mapping_key=None,
                minvalue=None, maxvalue=None, chioces=None, autominvalue=False, automaxvalue=False):
    """
        获取request参数
        param key: 参数名
        param type: 参数类型
        param required: 参数是否必须
        param mapping_key: request.xxx (args, form, headers, values)
        param minvalue: 限制参数最小值
        param maxvalue: 限制参数最大值
        param chioces: 给定参数选项,(元组)
        param autominvalue 值小于minvalue则自动调整为minvalue
        param automaxvalue 值大于maxvalue则自动调整为maxvalue
    """
    mapping = getattr(request, mapping_key, {})
    if required is True:
        if mapping:
            if mapping.get(key, '') == '':
                abort(400, "missing param {}".format(key))

    try:
        if required is True and key not in mapping:
            print("missing param {}".format(key))
            abort(400, "missing param {}".format(key))
    except Exception as e:
        abort(400, "missing param {}".format(key))
    
    try:
        value = mapping.get(key, default)
    except Exception as e:
        abort(400, "missing param {}".format(key))

    if type is not None:
        try:
            value = type(value)
        except (ValueError, TypeError):
            print("invild param type {}, {} needed".format(key, type))
            abort(400, "invile param type {}, {} needed".format(key, type))
        except Exception as e:
            print(e)
            abort(500)

    if minvalue is not None and value < minvalue:
        if autominvalue is True:
            value = minvalue
        else:
            abort(400, "param {} less than minvalue {}".format(key, minvalue))

    if maxvalue is not None and value > maxvalue:
        if automaxvalue is True:
            value = maxvalue
        else:
            abort(400, "param {} bigger than maxvalue {}".format(key, maxvalue))

    if chioces is not None and value not in chioces:
        abort(400, "params {} is not available".format(key))

    return value


request_args = partial(get_param, mapping_key="args")
request_form = partial(get_param, mapping_key="form")
request_values = partial(get_param, mapping_key="values")
request_headers = partial(get_param, mapping_key="headers")
request_jsons = partial(get_param, mapping_key="json")

