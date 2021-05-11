from flask import redirect
from flask_admin import Admin
from ..urls import MethodView
from .site.auth import login_user
from .site.models import *
from .site.views import *
from navycut.orm import db
from ..utils.security import check_password_hash

class _AdminLoginView(MethodView):
    def get(self):
        return self.render("admin/_adm_login.html")
    def post(self):
        username = self.request.form.get('username')
        password = self.request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if not user: return "Invalid username"
        if not check_password_hash(user.password, password): return "Invalid password"
        login_user(user)
        return redirect('/admin')


class NavycutAdmin(Admin):
    # def __init__(self, app=None):
    #     if app is not None: self.init_app(app)
    #     else: super(NavycutAdmin, self).__init__(self.app, template_mode="bootstrap4", index_view=_NavAdminIndexView())

    def init_app(self, app):
        self.app = app
        self._add_admin_login_view()
        super(NavycutAdmin, self).__init__(self.app, template_mode="bootstrap4", index_view=NavAdminIndexView())
        self._register_administrator_model()
    # def _add_view(self, model):
    #     current_app.admin.rm(model)

    # def register_model(self, model):
    #     with self.app.app_context():
    #         self._add_view(model)
    def _register_administrator_model(self):
        self.register_model(User, category="Users")
        self.register_model(Group, category="Users")

    def register_model(self, model, category=None) -> bool:
        """
        register the app specific model with the admin
        :param model: 
            specific model to register.
        """
        # model_fields:list = list(column.name for column in model.__table__.columns)
        # _all_image_fields = list(filter(None, list(field if field.endswith("_image") or field.endswith("_picture") else None for field in model_fields)))
        # if len(_all_image_fields): 
        #     self.add_view(NCSpecialModelView(model, db.session, category=category))
        #     return True
        self.add_view(NCSpecialModelView(model, db.session, category=category))
        return True

    def _add_admin_login_view(self):
        self.app.add_url_rule('/admin/login', view_func=_AdminLoginView.as_view("admin_login"), methods=['POST', 'GET'])

admin:NavycutAdmin = NavycutAdmin()
# admin.register_model(User, category="Users")
# admin.register_model(Group, category="Users")