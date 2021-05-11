from navycut.utils.server import create_wsgi_app
from os import environ


# Web server gateway interface
# use gunicorn wsgi server to run this app

#define your default settings file here:
# settings_file = "souvik.settings"

environ.setdefault("NAVYCUT_SETTINGS_MODULE", "souvik.settings")

application = create_wsgi_app()