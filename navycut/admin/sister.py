from navycut.core.app_config import AppSister
from . import admin

class AdminSister(AppSister):
    extra_ins = (admin,) # extra ins shoud have inbuild "init_app" method.