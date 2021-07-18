from navycut.core.app_config import AppSister
from . import admin
from .urls import url_patterns
import typing as t

if t.TYPE_CHECKING:
    from navycut import urls

class AdminSister(AppSister):
    name = "admin_auth_sister"
    url_pattern:t.Tuple[t.List[t.Union["urls.url", "urls.path", "urls.include"]]] = (url_patterns, )
    extra_ins = (admin,) # extra ins shoud have inbuild "init_app" method.