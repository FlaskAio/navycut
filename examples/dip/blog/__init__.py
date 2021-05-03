"""
Do not change anything if you dont have enough knowledge 
how to handle it, otherwise it may mess the server.
"""

from navycut.core import SisterApp
from os.path import abspath
from pathlib import Path
from .urls import url_patterns
from . import models
from . import views
from . import admin

__basedir__ = Path(abspath(__file__)).parent

_config__dict = {
    "import_name" : "blog",
    "name" : __name__,
    "template_folder" : __basedir__ / "templates",
    "static_folder" : __basedir__ / "static",
    "static_url_path" : "/blog/static/",
    "models" : models,
    "views" : views,
    "admin" : admin,
    "url_prefix" : "/blog",
}

app = SisterApp(_config__dict)

app.add_url_pattern(url_patterns)