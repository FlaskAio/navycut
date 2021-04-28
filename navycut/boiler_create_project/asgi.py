import settings
from navycut.utils.server import create_asgi_app


# asynchronous server gateway interface
# use uvicorn server to run this app
application = create_asgi_app(settings)