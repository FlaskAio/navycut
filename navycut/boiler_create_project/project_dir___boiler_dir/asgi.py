from navycut.utils.server import create_asgi_app
from os import environ


# Asynchronus server gateway interface
# use uvicorn asgi server to run this app

#define your default settings file here:
environ.setdefault("NAVYCUT_SETTINGS_MODULE", "project_name___boiler_var.settings")

application = create_asgi_app()