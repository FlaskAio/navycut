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
PROJECT_NAME = "default_project"

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

CORS_RESOURCES:t.Union[dict, list] = {}