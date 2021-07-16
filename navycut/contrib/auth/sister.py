from navycut.core.app_config import AppSister
from . import login_manager

class AuthSister(AppSister):
    extra_ins = (login_manager, )