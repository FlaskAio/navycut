from flask_login import LoginManager
from flask_admin import Admin
from .views import NavAdminIndexView
from .model import BaseUser
from ._routes import _admin_bp



class NavykutAdmin:
    def __init__(self, app):
        self.app = app
        self.app.register_blueprint(_admin_bp)
        self.login_manager = LoginManager(self.app)
        self.login_manager.login_view = 'routes.admin_login'
        @self.login_manager.user_loader
        def _load_user(user_id):
            return BaseUser.query.get(int(user_id))
        
        self.navAdmin = Admin(self.app, template_mode="bootstrap4", index_view=NavAdminIndexView())