# -*- coding: utf-8 -*-
"""
Description: 关于 
Date: 2019-12-13
Author: xgf
"""
import datetime

from flask import Blueprint, render_template
from flask.views import MethodView

from models.users.users import Admin, Images

bp = Blueprint('bp_about', __name__)


class About(MethodView):
    """关于"""
    def get(self):
        about = Admin.query.filter_by(is_use=True).first()
        item = about.to_admin()

        return render_template('about/about.html', item=item)


bp.add_url_rule('/', view_func=About.as_view('about'))
