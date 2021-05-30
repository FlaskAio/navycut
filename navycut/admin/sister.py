from os import path
from pathlib import Path
from navycut.core.app_config import SisterApp
from . import admin


_basedir = Path(path.abspath(__file__)).parent.parent

config__dict:dict = dict(
        import_name = __name__,
        name = "admin",
        static_folder =  _basedir / "static",
        static_url_path = "/",
        url_prefix = "/",
        template_folder = _basedir / "templates",
)

app = SisterApp(config__dict)
admin.init_app(app)