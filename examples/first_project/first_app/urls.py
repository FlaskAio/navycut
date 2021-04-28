from .views import *
from navykut.urls import path

url_patterns = [
    path("" , IndexView, "index"),
]