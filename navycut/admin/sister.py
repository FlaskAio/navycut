from os import path
from pathlib import Path
from navycut.core.app_config import SisterApp
from . import admin


_basedir = Path(path.abspath(__file__)).parent.parent

app = SisterApp(name="adminapp",
                import_name= __name__,
                template_folder=_basedir / "templates",
                static_folder=_basedir / "static",
                static_url_path="/",
                url_prefix="/",)

admin.init_app(app)