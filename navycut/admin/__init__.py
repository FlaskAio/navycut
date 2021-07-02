from flask import redirect, flash
from flask.globals import request
from flask.templating import render_template
from flask_admin import Admin
from ..auth import login_user, logout_user
from .site.models import *
from .site.views import *
from .site.forms import *
from navycut.orm import sql
from ..utils.security import check_password_hash


def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user: 
            flash("Invalid username")
            return redirect("/admin/login")
            
        if not check_password_hash(user.password, form.password.data): 
            flash ("Invalid password")
            return redirect("/admin/login")

        login_user(user)
        return redirect('/admin')
    return render_template("admin/_adm_login.html", form=form)


def admin_logout():
    if request.user.is_authenticated:
        logout_user()
    flash("User logged out successfully")
    return redirect("/admin/login")


class NavycutAdmin(Admin):
    def __init__(self,app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self._add_admin_login_view()
        super(NavycutAdmin, self).__init__(self.app, template_mode="bootstrap4", index_view=NavAdminIndexView())
        self._register_administrator_model()

    def _register_administrator_model(self):
        self.register_model(User, category="Users")
        self.register_model(Group, category="Users")

    def register_model(self, model, custom_view=None, category=None) -> bool:
        """
        register the app specific model with the admin
        :param model: 
            specific model to register.
        :param custom_view:
            The custom Model View class.
        
        :for example ::
            from .models import Blog
            admin.register_model(Blog)
        """
        if custom_view is not None:
            self.add_view(custom_view(model, sql.session, category=category))
        self.add_view(NCAdminModelView(model, sql.session, category=category))
        return True

    def _add_admin_login_view(self):
        self.app.add_url_rule('/admin/login/', view_func=admin_login, methods=['POST', 'GET'])
        self.app.add_url_rule('/admin/logout/', view_func=admin_logout, methods=['POST', 'GET'])

admin:NavycutAdmin = NavycutAdmin()