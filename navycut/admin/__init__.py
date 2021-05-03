from flask import redirect
from flask_login import current_user
from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from ..urls import MethodView
from .site.auth import login_manager, login_user
from .site.models import *
from ..utils.security import check_password_hash
# from .views import NavAdminIndexView
# from .model import BaseUser
# from ._routes import _admin_bp

class _NavAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return redirect('/admin/login')

class _AdminLoginView(MethodView):
    def get(self):
        return self.render("_admin/_adm_login.html")
    def post(self):
        username = self.request.form.get('username')
        password = self.request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if not user: return "Invalid username"
        if not check_password_hash(user.password, password): return "Invalid password"
        login_user(user)
        return redirect('/admin')


class NavycutAdmin(Admin):
    def __init__(self, app):
        self.app = app
        login_manager.init_app(self.app)
        self._add_admin_login_view()
        super(NavycutAdmin, self).__init__(self.app, template_mode="bootstrap4", index_view=_NavAdminIndexView())

    def register_model(self,model):
        """
        register the app specific model with the admin
        :param model: specific model to register.
        """
        self.add_view(ModelView(model, self.app.models.session))

    def _add_admin_login_view(self):
        self.app.add_url_rule('/admin/login', view_func=_AdminLoginView.as_view("admin_login"), methods=['POST', 'GET'])