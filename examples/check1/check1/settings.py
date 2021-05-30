from pathlib import Path
from os.path import abspath

# defining the default import name for flask:
IMPORT_NAME = __name__

#defining the actual project name:
PROJECT_NAME = "check1"


#defining the base directory
BASE_DIR = Path(abspath(__file__)).parent.parent

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
SECRET_KEY = r"GU%6x$bjYn<R>05ak+]1/>pXDF[x7cD]d1D!>N6EfaekMHPOWd}:4" #should generate randomly at the time of creation.


#available installed app add here to bloom.
INSTALLED_APPS = [ # should change to first_app to get the app.
    "navycut.admin.sister",
    "navycut.helpers.static_server.sister",
    #"first_app.sister", 
]

ALLOWED_HOST = [ # 
    '127.0.0.1', 
]