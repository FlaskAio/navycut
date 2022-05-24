from navycut.urls import url
from . import views
import typing as t

if t.TYPE_CHECKING:
    from navycut.typing import ncUrlPatterns

urlpatterns:"ncUrlPatterns" = [

    url("/login/", views.admin_login, "admin_login"),
    url("/logout/", views.admin_logout, "admin_logout")
]