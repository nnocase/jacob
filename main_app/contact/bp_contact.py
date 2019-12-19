# -*- coding: utf-8 -*-
"""
Description: 留言或友链申请
Date: 2019-12-13
Author: xgf
"""
import datetime 

from flask import Blueprint, render_template
from flask.views import MethodView

bp = Blueprint('bp_contact', __name__)


class Contact(MethodView):
    """留言"""
    def get(self):

        return render_template('contact/contact.html')

    def post(self):
        pass


bp.add_url_rule('/', view_func=Contact.as_view('contact'))
