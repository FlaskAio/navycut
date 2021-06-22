from pathlib import Path
from os.path import abspath

# defining the default import name for flask:
IMPORT_NAME = __name__

#defining the actual project name:
PROJECT_NAME = "check2"


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
SECRET_KEY = r"nKXOtseZUJ;m;<iHvbXR:$jxLS%/C]bvSJ:sGM{0oZImNbrVPVL*x" #should generate randomly at the time of creation.


#available installed app add here to bloom.
INSTALLED_APPS = [ # should change to first_app to get the app.
    "navycut.admin.sister.AdminSister",
    "navycut.helpers.upload_server.sister.UploadserverSister",
    "app1.sister.App1Sister", 
]

ALLOWED_HOST = [ # 
    '127.0.0.1', 
]

MAIL_USING_SMTP = True

SMTP_CONFIGURATION = {
    "host" : "smtp.gmail.com",
    "post" : 587,
    "username" : "aniketsarkar1998@gmail.com",
    "password" : "none",
    "is_using_ssl" : False,
    "is_using_tls" : True,
    "options" : {}
} 