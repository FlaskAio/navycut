from os import environ
environ.setdefault("NAVYCUT_SETTINGS_MODULE", "check2.settings")


# Web server gateway interface
# use gunicorn wsgi server to run this app

#define your default settings file here:

from navycut.utils.server import create_wsgi_app


application = create_wsgi_app()