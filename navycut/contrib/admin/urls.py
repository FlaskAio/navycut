from navycut.urls import url
from . import views

url_patterns = [
    url("/admin/login/", views.admin_login, "admin_login"),
    url("/admin/logout/", views.admin_logout, "admin_logout")
]