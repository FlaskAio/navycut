from navycut.urls import path
from .views import *

url_patterns = [
    path("" , IndexView, "index"),
]