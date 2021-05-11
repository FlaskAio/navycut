from navycut.utils.server import create_asgi_app


# asynchronous server gateway interface
# use uvicorn asgi server to run this app

#define your default settings file here:
settings_file = "souvik.settings"

application = create_asgi_app(settings_file)