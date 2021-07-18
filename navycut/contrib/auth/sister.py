from navycut.core.app_config import AppSister
from . import login_manager

class AuthSister(AppSister):
    seize_power = True
    name = "auth_service_sister"
    extra_ins = (login_manager, )