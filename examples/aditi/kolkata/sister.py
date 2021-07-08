"""
Do not change anything if you dont have enough knowledge 
how to handle it, otherwise it may mess the server.
"""

from navycut.core import AppSister
from navycut.utils import path
from pathlib import Path
from .urls import url_patterns


__basedir__ = path.abspath(__file__).parent


class KolkataSister(AppSister):
    name = "kolkata"
    template_folder = __basedir__ / "templates"
    static_folder = __basedir__ / "static"
    static_url_path = "/static"
    url_prefix = "/kolkata"
    url_pattern = (url_patterns, )
    import_app_feature = True