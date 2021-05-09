from pathlib import Path
from os.path import abspath

# defining the default import name for flask:
IMPORT_NAME = __name__

#defining the actual project name:
PROJECT_NAME = "project_name___boiler_var"


#defining the base directory
BASE_DIR = Path(abspath(__file__)).parent.parent

#app debug state:
DEBUG = True

#defining the base database configuration.
DATABASE = {
    "engine" : "sqlite3",
    "database": BASE_DIR / "navycut.sqlite3"
}

#defining the navycut app secret key
SECRET_KEY = "__secretkey_____boiler_var" #should generate randomly at the time of creation.


DEFAULT_INDEX = True # if True": it will show the default index page, to use your own index please set it to False.

#available installed app add here to bloom.
INSTALLED_APPS = [ # should change to first_app to get the app.
    #"first_app", 
]

ALLOWED_HOST = [ # 
    '127.0.0.1', 
]