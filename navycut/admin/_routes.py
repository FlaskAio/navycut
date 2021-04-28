
from flask import request, render_template, Blueprint, url_for, redirect
from flask_login import login_user
from flask.views import MethodView
from os.path import abspath
from pathlib import Path
from .model import BaseUser
from werkzeug.security import check_password_hash

class _BaseIndexView(MethodView):
    def get(self):
        return render_template("_index.html")

_basedir = Path(abspath(__file__)).parent.parent

_admin_bp = Blueprint(name="admin_bp", import_name=__name__, template_folder=_basedir/'templates')

# @_admin_bp.route("/")
# def _index():
#     return render_template('index.html')

@_admin_bp.route('/admin/login', methods=['GET', 'POST'])
def _admin_login():
    if request.method == 'GET':
        return render_template('admin/login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = BaseUser.query.filter_by(username=username).first()
        if not user: return "Invalid username"
        if not check_password_hash(user.password, password): return "Invalid password"
        login_user(user)
        return redirect('/admin')
        # return redirect(url_for('_admin_bp._admin_login', next=request.url))    