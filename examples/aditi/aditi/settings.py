from navycut.utils import path

# defining the default import name for flask:
IMPORT_NAME = __name__

#defining the actual project name:
PROJECT_NAME = "aditi"


#defining the base directory
BASE_DIR = path.abspath(__file__).parent.parent

TEMPLATE_DIR = BASE_DIR / "templates"

#app debug state:
DEBUG = True

#defining the base database configuration.
DATABASE = dict(
    engine = "navycut.orm.sqla.engine.sqlite3",
    creds = dict(
        host = None,
        username = None,
        password = None,
        database = BASE_DIR / "navycut.sqlite3"
    )
)

#defining the navycut app secret key
SECRET_KEY = r"f7>Rn2eJli}>kVr7Hj@6^$&2P35Bx^>C^}FsOKG94SER!lwgtx[Wa" #should generate randomly at the time of creation.


#available installed app add here to bloom.
INSTALLED_APPS = [ # should change to first_app to get the app.
    "navycut.orm.sqla",
    "navycut.contrib.cors",
    "navycut.contrib.auth",
    "navycut.contrib.mail",
    "navycut.contrib.admin",
    "navycut.helpers.upload_server",
    "aniket",
    "sarkar",
    "kolkata",
    "plassey"
]

MIDDLEWARE = [
    "navycut.middleware.ipfilter.IPFilterMiddleware",
]

ALLOWED_HOST = [ # 
    '127.0.0.1', 
    "192.168.0.107"
]

# Email Configuration

# Host for sending email.
EMAIL_HOST = 'smtp.gmail.com'

# Port for sending email.
EMAIL_PORT = 587

# Whether to send SMTP 'Date' header in the local time zone or in UTC.
EMAIL_USE_LOCALTIME = False

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = 'aniketsarkar1998@gmail.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EXTRA_ARGS = None

CORS_RESOURCES = {}