from navykut.core import app, models
from pathlib import Path
from os.path import abspath

# import your custom app here

# from first_app import first_app

# ____end of custom app importing

#defining the base directory
__basedir__ = Path(abspath(__file__)).parent

#app debug state:
__appdebug__ = False

#defining the base database configuration.
__database__ = {
    "engine" : "sqlite3",
    "database": __basedir__ / "navykut.sqlite3"
}

#defining the navykut app secret key
__secretkey__ = "__secretkey_____boiler_var" #should generate randomly at the time of creation.

#default index view.
__indexview__ = None # None means seted to default. change it with your any app's view function.
# __indexview__ = first_app.views.IndexView

#available installed app add here to bloom.
__installedapp__ = [
    #first_app, # should change to first_app to get the app.
]
