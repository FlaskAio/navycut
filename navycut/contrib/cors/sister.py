from navycut.core.app_config import AppSister
from . import cors


class CorsSister(AppSister):
    import_name = __name__
    name = "cors_custom_sister"
    extra_ins = (cors, )