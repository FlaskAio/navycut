from pathlib import Path
from os.path import abspath

# defining the default import name for flask:
IMPORT_NAME = __name__

#defining the actual project name:
PROJECT_NAME = "souvik"

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
SECRET_KEY = r"c?zK/;b4Mdk5;&cu{74H}W5;6oo<T?Qvp?U4T@VB@ftTs:2s40N/$" #should generate randomly at the time of creation.


DEFAULT_INDEX = True # if True": it will show the default index page, to use your own index please set it to False.

#available installed app add here to bloom.
INSTALLED_APPS = [ # should change to first_app to get the app. 
    "navycut.helpers.static_server",
    # "blogs",
    "sarkar",
]

ALLOWED_HOST = [ # 
    '127.0.0.1', 
]