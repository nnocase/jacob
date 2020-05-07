# -*- coding: utf-8 -*-
"""
Description: 留言或友链申请
Date: 2019-12-13
Author: xgf
"""
import traceback

from flask import Blueprint, render_template, redirect, flash, url_for
from flask.views import MethodView

from models.posts.posts import Messages
from lib._flask import request_form, request_args
from models.base import db

bp = Blueprint('bp_contact', __name__)


class Contact(MethodView):
    """留言"""
    def get(self):

        return render_template('contact/contact.html')

    def post(self):
        name = request_form('name', type=str, required=True)
        email = request_form('email', type=str)
        url = request_form('url', type=str, default='')
        message = request_form('message', type=str)

        mess = Messages(name=name, email=email, url=url, message=message)
        try:
            db.session.add(mess)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(traceback.format_exc())
            flash(u'发送成功', 'danger')
            return redirect(url_for('bp_contact.contact'))
        
        flash(u'发送成功', 'success')
        return redirect(url_for('bp_contact.contact'))


bp.add_url_rule('/', view_func=Contact.as_view('contact'))
