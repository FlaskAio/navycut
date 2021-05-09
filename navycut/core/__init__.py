""" import default app and default models from here """

from .app_config import Navycut
from .app_config import SisterApp


app = Navycut()
settings = app._import_settings_from_project_dir()
app._add_config(settings)
app._configure_core_features()
app._perform_app_registration()