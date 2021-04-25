from navycut.core import SisterApp
from os.path import abspath
from pathlib import Path

from .urls import url_patterns
from . import models
from . import views

__basedir__ = Path(abspath(__file__)).parent

_config__dict = {
    "import_name" : "['<import_name>']",
    "name" : __name__,
    "template_folder" : __basedir__ / "templates",
    "static_folder" : __basedir__ / "static",
    "static_url_path" : "/['<import_name>']/static/",
    "models" : models,
    "views" : views,
}

['<import_name>'] = SisterApp(_config__dict)

['<import_name>'].add_url_pattern(url_patterns)