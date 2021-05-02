from navycut.core import SisterApp
from os.path import abspath
from pathlib import Path

from .urls import url_patterns
from . import models
from . import views
from . import admin

__basedir__ = Path(abspath(__file__)).parent

_config__dict = {
    "import_name" : "blogs",
    "name" : __name__,
    "template_folder" : __basedir__ / "templates",
    "static_folder" : __basedir__ / "static",
    "static_url_path" : "/blogs/static/",
    "models" : models,
    "views" : views,
    "admin" : admin,
    "url_prefix" : "/blogs",
}

app = SisterApp(_config__dict)

app.add_url_pattern(url_patterns)