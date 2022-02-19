from navycut.core.app_config import AppSister
from . import admin
from .urls import urlpatterns
import typing as t

if t.TYPE_CHECKING:
    from navycut.typing import ncUrlPattern

class AdminSister(AppSister):
    name = "admin_auth_sister"
    url_pattern:"ncUrlPattern" = (urlpatterns, )
    extra_ins = (admin,) # extra ins shoud have inbuild "init_app" method.