from flask import Flask, Blueprint
from flask_migrate import Migrate
from navycut.urls import MethodView
from importlib import import_module
from navycut.orm._fod.engine import _SQLITE_ENGINE, _MYSQL_ENGINE
from os.path import abspath
from pathlib import Path
from ..admin.site.auth import login_manager
from ..orm.db import db
from ..admin import admin

_basedir = Path(abspath(__file__)).parent.parent

class _BaseIndexView(MethodView):
    def get(self):
        return self.render("_index.html")

class Navycut(Flask):
    def __init__(self, settings:object=None):
        super(Navycut, self).__init__(__name__, 
                    template_folder=_basedir / 'templates',
                    static_folder=str(_basedir / "static"),
                    static_url_path="/static")
        self.settings = settings

    def _add_config(self, settings) -> None:
        self.settings = settings
        self.import_name = settings.IMPORT_NAME
        self.project_name = settings.PROJECT_NAME
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        self.config["BASE_DIR"] = settings.BASE_DIR
        self.config['SECRET_KEY'] = settings.SECRET_KEY
        self.config['DEBUG'] = settings.DEBUG
        self.debug = settings.DEBUG        
        if settings.DATABASE.get('engine').lower() == "sqlite" or "sqlite3":
            self.config['SQLALCHEMY_DATABASE_URI'] = _SQLITE_ENGINE(settings.DATABASE.get('database'))
        elif settings.DATABASE.get('engine').lower() == "mysql":
            self.config['SQLALCHEMY_DATABASE_URI'] = _MYSQL_ENGINE(settings.DATABASE.get('database'))
        self._configure_default_index()
    
    def _configure_core_features(self):
        #add all the core features of navycut app here.
        self.initIns(db)
        self.initIns(login_manager)
        self.initIns(admin)
        Migrate(self, db)

    def _perform_app_registration(self):
        self._registerApp(self.settings.INSTALLED_APPS)

    def _configure_default_index(self):
        if self.settings.DEFAULT_INDEX is not False and self.settings.DEBUG is not False:
            self.add_url_rule(rule="/", view_func=_BaseIndexView.as_view("index"), methods=['GET'])
        else: pass
    
    def initIns(self, ins) -> bool:
        ins.init_app(self)
        return True

    def _import_app(self, app:str):
        try: app = import_module(app)
        except AttributeError: raise AttributeError(f"{app} not installed at {self.config.get('BASE_DIR')}. Dobule check the app name. is it really {app} ?")
        return getattr(app, 'app')

    def _registerApp(self, _appList:list):
        for str_app in _appList: 
            try: app = self._import_app(f"{self.project_name}.{str_app}")
            except: app = self._import_app(str_app)
            self.register_blueprint(app, url_prefix=app.url_prefix)


    def _import_settings_from_project_dir(self) -> object:
        try: 
            settings = import_module('settings')
            return settings
        except Exception: 
            try:
                name = import_module('name').__file__
                proj_dir =  Path(abspath(name)).parent
                settings = import_module(f'{str(proj_dir).rsplit("/", 1)[1]}.settings')
                return settings
            except ModuleNotFoundError: raise AttributeError("neither name.py nor settings.py found.")
        

    def debugging(self,flag=False) -> None:
        self.debug = flag

    def __repr__(self):
        return self.import_name

class SisterApp(Blueprint):
    def __init__(self, arg_dict:dict, *wargs, **kwargs):
        super(SisterApp, self).__init__(name=str(arg_dict['name']),
                                        import_name=str(arg_dict['import_name']),
                                        template_folder=str(arg_dict['template_folder']),
                                        static_folder=str(arg_dict['static_folder']),
                                        static_url_path=str(arg_dict['static_url_path']),
                                        *wargs, **kwargs)
        self.url_prefix = arg_dict['url_prefix']
        self._name = str(arg_dict['import_name'])
    
    def add_url_pattern(self, pattern_list:list):
        for url_path in pattern_list:
            self.add_url_rule(rule=url_path.url, view_func=url_path.views.as_view(url_path.name), methods=['GET','PUT', 'DELETE', 'POST', 'HEAD'])

    def import_app_features(self) -> None:
        import_module(f"{self._name}.models", package=None)
        import_module(f"{self._name}.admin", package=None)

    def __repr__(self):
        return self.import_name