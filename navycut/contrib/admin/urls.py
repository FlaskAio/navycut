from navycut.urls import url
from . import views
import typing as t

if t.TYPE_CHECKING:
    from navycut.typing import ncUrlPatterns

url_patterns:"ncUrlPatterns" = [

    url("/admin/login/", views.admin_login, "admin_login"),
    url("/admin/logout/", views.admin_logout, "admin_logout")
]