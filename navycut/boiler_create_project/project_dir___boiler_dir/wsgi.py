from navycut.utils.server import create_wsgi_app


# Web server gateway interface
# use gunicorn wsgi server to run this app

#define your default settings file here:
settings_file = "project_name___boiler_var.settings"

application = create_wsgi_app(settings_file)