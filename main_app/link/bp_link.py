# -*- encoding -*-
"""
Description: 友链
Date: 2019-12-16
Author: xgf
"""
import datetime

from flask import Blueprint, render_template
from flask.views import MethodView

from models.posts.posts import Links

bp = Blueprint('bp_link', __name__)


class List(MethodView):
    """友链列表"""
    def get(self):

        return render_template('link/link.html')


bp.add_url_rule('/', view_func=List.as_view('list'))
