from a2wsgi import WSGIMiddleware
from navycut.core import app

def create_wsgi_app():
    app._attach_settings_modules()
    app.debugging(False)
    return app
    

def create_asgi_app(settings_file:str):
    return WSGIMiddleware(create_wsgi_app(settings_file))