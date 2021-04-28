from navycut.core import SisterApp
from os.path import abspath
from pathlib import Path

from .urls import url_patterns
from . import models
from . import views

__basedir__ = Path(abspath(__file__)).parent

_config__dict = {
    "import_name" : "import_name___boiler_var",
    "name" : __name__,
    "template_folder" : __basedir__ / "templates",
    "static_folder" : __basedir__ / "static",
    "static_url_path" : "/import_name___boiler_var/static/",
    "models" : models,
    "views" : views,
    "url_prefix" : "/import_name___boiler_var",
}

import_name___boiler_var = SisterApp(_config__dict)

import_name___boiler_var.add_url_pattern(url_patterns)