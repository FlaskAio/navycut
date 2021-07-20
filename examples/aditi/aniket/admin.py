from navycut.contrib import admin
from .models import *
from navycut.contrib.admin.site.views import NCAdminModelView

# admin.register_model(Blog)
admin.register_model(Author)
admin.register_model(ExtraUser)

class BlogAdminView(NCAdminModelView):
    pass
    excluded_fields = ["name", "body"]


admin.register_model(Blog, BlogAdminView)