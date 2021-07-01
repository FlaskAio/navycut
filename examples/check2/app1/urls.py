from navycut.urls import path, url, include
from . import views
# from extra_app 

url_patterns = [
    path("" , views.IndexView, "index"),
    path("/register", views.AuthView, "auth"),
    url("/home", views.home, "home"),
    url("/mail", views.send_email, "mail"),
    include("/nord", "nord.urls")
]