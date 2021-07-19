from navycut.core import app
from asgiref.wsgi import WsgiToAsgi



def create_wsgi_app():
    app._attach_settings_modules()
    app.debugging(False)
    return app
    

def create_asgi_app():
    return WsgiToAsgi(create_wsgi_app())