from a2wsgi import WSGIMiddleware
from navycut.core import app
from importlib import import_module
from ..errors.server import SettingsFileNotFoundError

def create_wsgi_app(settings_file:str):
    app.debugging(False)
    try: settings = import_module(settings_file)
    except ModuleNotFoundError: raise SettingsFileNotFoundError(settings_file.split(".")[1], f"{app.config.get('BASE_DIR')}/{app.project_name}") 
    app._add_config(settings)
    return app
    

def create_asgi_app(settings_file:str):
    return WSGIMiddleware(create_wsgi_app(settings_file))