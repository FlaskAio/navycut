from os import environ
environ.setdefault("NAVYCUT_SETTINGS_MODULE", "check2.settings")

# Asynchronus server gateway interface
# use uvicorn asgi server to run this app

#define your default settings file here:

from navycut.utils.server import create_asgi_app

application = create_asgi_app()