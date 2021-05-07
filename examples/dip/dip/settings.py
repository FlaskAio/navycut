from pathlib import Path
from os.path import abspath


#defining the base directory
__basedir__ = Path(abspath(__file__)).parent.parent

#app debug state:
__appdebug__ = True

#defining the base database configuration.
__database__ = {
    "engine" : "sqlite3",
    "database": __basedir__ / "navycut.sqlite3"
}

#defining the navycut app secret key
__secretkey__ = "8r%8Vn{OfC:#5u%r%uho8r?QK1*G@6Gt;E8iO<ab4{9zdgu}u:S#e" #should generate randomly at the time of creation.

#default index view.
__indexview__ = None # None means seted to default. change it with your any app's view function.
# __indexview__ = first_app.views.IndexView

__defaultindex__ = True # if True": it will show the default index page, to use your own index please set it to False.

#available installed app add here to bloom.
__installedapp__ = [
    "blog", # should change to first_app to get the app.
]

__allowedhost__ = [ # 
    '127.0.0.1', 
]