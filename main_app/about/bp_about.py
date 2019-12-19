# -*- coding: utf-8 -*-
"""
Description: 关于 
Date: 2019-12-13
Author: xgf
"""
import datetime 

from flask import Blueprint, render_template
from flask.views import MethodView

bp = Blueprint('bp_about', __name__)


class About(MethodView):
    """关于"""
    def get(self):

        return render_template('about/about.html')


bp.add_url_rule('/', view_func=About.as_view('about'))
