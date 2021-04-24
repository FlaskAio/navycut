from flask import Flask
from ..database.engine import _SQLITE_ENGINE, _MYSQL_ENGINE
# from os.path import abspath
# from pathlib import Path

# _basedir = Path(abspath(__file__)).parent.parent


_appConfig__default:dict = {
    'SECRET_KEY': "b40a0e070c1519495d6540676cda7e3f22c0488e64af8e89a4222f77b3b7224a",
    'SQLALCHEMY_DATABASE_URI' : "",
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
}


class Navycut(Flask):
    def __init__(self, importName,
            models=None):
        self.importName = importName.lower()
        self.models = models
        super(Navycut, self).__init__(self.importName)
        for key, value in _appConfig__default.items(): self.config[key] = value
        if self.models: models.init_app(self)

    def addConfig(self, settings) -> None:
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        self.config["BASE_DIR"] = settings.__basedir
        self.config['SECRET_KEY'] = settings.__secretkey
        #for database config: 
        if settings.__database.get('engine').lower() == "sqlite" or "sqlite3":
            self.config['SQLALCHEMY_DATABASE_URI'] = _SQLITE_ENGINE(settings.__database.get('database'))
        elif settings.__database.get('engine').lower() == "mysql":
            self.config['SQLALCHEMY_DATABASE_URI'] = _MYSQL_ENGINE(settings.__database.get('database'))
    
    def initIns(self, ins):
        ins.init_app(self)
        return True

    def initmodels(self):
        self.init_app(self.models)

    def registerApp(self, extraApp):pass


    def debugging(self,flag=False):
        self.debug = flag
        return True

    def __repr__(self):
        return self.importName