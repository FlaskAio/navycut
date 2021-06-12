from navycut.admin import admin
from navycut.admin.site.views import NCAdminModelView
from .models import Blog, Polls

class PollsModelView(NCAdminModelView):
    excluded_fields = ['picture', "", ]


admin.register_model(Blog)
admin.register_model(Polls, PollsModelView)