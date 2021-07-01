from navycut.urls import path, url
from . import views

url_patterns = [
    # path("" , views.IndexView, "index"),
    url("", views.homepage, "index"),
    url("/another", views.another_page, "another"),
    url("/aditi", views.aditi, "aditi")
]