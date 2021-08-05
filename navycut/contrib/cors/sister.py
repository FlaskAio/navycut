from navycut.core.app_config import AppSister
from . import cors


class CorsSister(AppSister):
    seize_power = True
    name = "cors_custom_sister"
    extra_ins = (cors, )