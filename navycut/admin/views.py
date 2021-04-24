from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask import redirect

class SecureModelView(ModelView):
    def is_accessible(self):
        return False
    def inaccessible_callback(self, name, **kwargs):
        return redirect('/admin/login')

class NavAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return False
    def inaccessible_callback(self, name, **kwargs):
        return redirect('/admin/login')