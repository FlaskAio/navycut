from os import environ
environ.setdefault("NAVYCUT_SETTINGS_MODULE", "project_name___boiler_var.settings")


# Web server gateway interface
# use gunicorn wsgi server to run this app

from navycut.utils.server import create_wsgi_app

application = create_wsgi_app()