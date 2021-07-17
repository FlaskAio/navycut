from navycut.utils import path

# defining the default import name for flask:
IMPORT_NAME = __name__

#defining the actual project name:
PROJECT_NAME = "project_name___boiler_var"


#defining the base directory
BASE_DIR = path.abspath(__file__).parent.parent

TEMPLATE_DIR = BASE_DIR / "templates"

#app debug state:
DEBUG = True

#defining the base database configuration.
DATABASE = {
    "engine" : "sqlite3",
    "creds" : {
        "host"     : None,
        "username" : None,
        "password" : None,
        "database" : BASE_DIR / "navycut.sqlite3"
    }
}

#defining the navycut app secret key
SECRET_KEY = r"__secretkey_____boiler_var" #should generate randomly at the time of creation.


#available installed app add here to bloom.
INSTALLED_APPS = [ # should change to first_app to get the app.
    "navycut.contrib.auth",
    "navycut.contrib.admin",
    "navycut.helpers.upload_server",
    #"first_app", 
]

MIDDLEWARE = [
    "navycut.middleware.ipfilter.IPFilterMiddleware",
    "navycut.contrib.admin.middleware.AdminAuthMiddleware",
]


ALLOWED_HOST = [ # 
    '127.0.0.1', 
]

# Email SMTP Configuration
MAIL_USING_SMTP = False

SMTP_CONFIGURATION = {
    "host" : None,
    "post" : None,
    "username" : None,
    "password" : None,
    "is_using_ssl" : None,
    "is_using_tls" : None,
    "options" : {}
} 

EXTRA_ARGS = None