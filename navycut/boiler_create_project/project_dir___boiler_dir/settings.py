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
__secretkey__ = "__secretkey_____boiler_var" #should generate randomly at the time of creation.


__defaultindex__ = True # if True": it will show the default index page, to use your own index please set it to False.

#available installed app add here to bloom.
__installedapp__ = [ # should change to first_app to get the app.
    #"first_app", 
]

__allowedhost__ = [ # 
    '127.0.0.1', 
]