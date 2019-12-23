# -*- encoding -*-
"""
Description: 友链
Date: 2019-12-16
Author: xgf
"""
from flask import Blueprint, render_template
from flask.views import MethodView

from models.posts.posts import Messages

bp = Blueprint('bp_link', __name__)


class List(MethodView):
    """友链列表"""
    def get(self):
        mess = Messages.query.filter_by(is_use=True).order_by(Messages.id.desc()).all()
        items = [m.to_admin() for m in mess]

        return render_template('link/link.html', items=items)


bp.add_url_rule('/', view_func=List.as_view('list'))
