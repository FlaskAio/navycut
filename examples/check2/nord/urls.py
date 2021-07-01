from navycut.urls import path, url
from . import views

url_patterns = [
    path("/" , views.IndexView, "index"),
    url("/home", views.home, "home")
]