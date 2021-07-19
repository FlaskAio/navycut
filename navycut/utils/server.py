from navycut.core import app
from asgiref.wsgi import WsgiToAsgi



def create_wsgi_app():
    """
    create the wsgi appliaction to run the project 
    using any wsgi server like gunicorn.
    """
    app._attach_settings_modules()
    app.debugging(False)
    return app
    

def create_asgi_app():
    """
    create the asgi appliaction to run the project 
    using any asgi server like uvicorn.
    """
    return WsgiToAsgi(create_wsgi_app())