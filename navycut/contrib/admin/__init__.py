from flask_admin import Admin
from .site.models import *
from .site.views import *
from .site.forms import *
from navycut.orm import sql


class NavycutAdmin(Admin):
    def __init__(self,app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
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

admin:NavycutAdmin = NavycutAdmin()