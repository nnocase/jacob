# -*- encoding -*- 
"""
Description: 首页
Author: xgf
Date: 2019-12-11
"""
import datetime

from flask import Blueprint, render_template
from flask.views import MethodView

from models.posts.posts import Posts
from lib._flask import request_form

bp = Blueprint('bp_home', __name__)


class Home(MethodView):
    """首页"""
    def get(self):
        posts = Posts.query.filter_by(is_use=True).all()
        items = [p.to_home() for p in posts]
        
        return render_template('home/index.html', items=items)


bp.add_url_rule('/', view_func=Home.as_view('home'))
