from navycut.core import AppInterface, app
from .urls import url_patterns
from .models import models

_config__dict = {
    "import_name" : "first_app",
    "name" : __name__,
    "template_folder" : app.config.get('BASE_DIR') / "first_app/templates",
    "static_folder" : app.config.get('BASE_DIR') / "first_app/static",
    "static_url_path" : "/first_app/static/",
    "models" : models,
}

first_app = AppInterface(_config__dict)

first_app.addUrlPattern(url_patterns)