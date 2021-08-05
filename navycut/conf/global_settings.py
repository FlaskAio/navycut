"""
Default Navycut settings. Override these with settings in the module pointed to
by the DJANGO_SETTINGS_MODULE environment variable.
"""

import typing as t


####################
# CORE             #
####################

# defining the default import name for flask:
IMPORT_NAME = __name__

#defining the actual project name:
PROJECT_NAME = "navycut_project"

BASE_DIR = None

TEMPLATE_DIR = None

#app debug state:
DEBUG = False

#defining the base database configuration.
DATABASE = {}

#defining the navycut app secret key
SECRET_KEY = None 


#available installed app add here to bloom.
INSTALLED_APPS = [ 
]

ALLOWED_HOST = [  
]

# Email Configuration
EMAIL_BACKEND = 'navycut.contrib.mail.backends.smtp.EmailBackend'

# Host for sending email.
EMAIL_HOST = 'localhost'

# Port for sending email.
EMAIL_PORT = 25

# Whether to send SMTP 'Date' header in the local time zone or in UTC.
EMAIL_USE_LOCALTIME = False

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
EMAIL_SSL_CERTFILE = None
EMAIL_SSL_KEYFILE = None
EMAIL_TIMEOUT = None
DEFAULT_FROM_EMAIL = 'webmaster@localhost'
EMAIL_FILE_PATH = None
EMAIL_DEFAULT_CHARSET = 'utf-8'

EXTRA_ARGS = None

CORS_RESOURCES:t.Union[dict, list] = {}