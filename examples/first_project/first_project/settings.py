from navycut.core import app, models
from pathlib import Path
from os.path import abspath

_Navycut__basedir = Path(abspath(__file__)).parent.parent

_Navycut__database = {
    "engine" : "sqlite3",
    "database": _Navycut__basedir / "navycut.sqlite3"
}

_Navycut__secretkey = "most_secret_key"

_Navycut__installedapp = [
    
]