from .views import *
from navycut.urls import path

url_patterns = [
    path("" , IndexView, "index"),
]