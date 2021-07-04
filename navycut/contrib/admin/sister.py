from navycut.core.app_config import AppSister
from . import admin
from .urls import url_patterns

class AdminSister(AppSister):
    url_pattern = (url_patterns, )
    extra_ins = (admin,) # extra ins shoud have inbuild "init_app" method.