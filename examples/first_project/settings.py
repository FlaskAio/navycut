from navycut.core import app, models
from pathlib import Path
from os.path import abspath
from . import first_app
# from first_project.first_app import first_app

__basedir__ = Path(abspath(__file__)).parent.parent

__database__ = {
    "engine" : "sqlite3",
    "database": __basedir__ / "navycut.sqlite3"
}

__secretkey__ = "most_secret_key"

__installedapp__ = [
    first_app.first_app, # should change to "first_app.__init__" to get the app.
]