from a2wsgi import WSGIMiddleware

def create_asgi_app(settings):
    settings.app.debugging(False)
    return WSGIMiddleware(settings.app)