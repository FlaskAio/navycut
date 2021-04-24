from flask import Flask, Blueprint
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
        self.config["BASE_DIR"] = settings.__basedir__
        self.config['SECRET_KEY'] = settings.__secretkey__
        #for database config: 
        if settings.__database__.get('engine').lower() == "sqlite" or "sqlite3":
            self.config['SQLALCHEMY_DATABASE_URI'] = _SQLITE_ENGINE(settings.__database__.get('database'))
        elif settings.__database__.get('engine').lower() == "mysql":
            self.config['SQLALCHEMY_DATABASE_URI'] = _MYSQL_ENGINE(settings.__database__.get('database'))
        #for custom app config:
        self.registerApp(settings.__installedapp__)
    
    def initIns(self, ins):
        ins.init_app(self)
        return True

    def initmodels(self):
        self.init_app(self.models)

    def registerApp(self, _appList:list):
        for app in _appList: self.register_blueprint(app, url_prefix="/"+str(app))

    def debugging(self,flag=False):
        self.debug = flag
        return True

    def __repr__(self):
        return self.importName

class AppInterface(Blueprint):
    def __init__(self, arg_dict:dict, *wargs, **kwargs):
        super(AppInterface, self).__init__(name=arg_dict['name'],
                                        import_name=arg_dict['import_name'],
                                        template_folder=arg_dict['template_folder'],
                                        static_folder=arg_dict['static_folder'],
                                        static_url_path=arg_dict['static_url_path'],
                                        *wargs, **kwargs)
        if arg_dict: self.models = arg_dict['models']

    @property
    def models(self):
        return self.models
    
    def add_url_pattern(self, pattern_list:list):
        for pattern in pattern_list:
            url, view, name = pattern
            self.add_url_rule(url, view_func=view.as_view(name), methods=['GET', 'PUT', 'DELETE', 'POST'])

    def __repr__(self):
        return self.import_name