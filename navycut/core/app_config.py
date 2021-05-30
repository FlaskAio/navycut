from flask import Flask, Blueprint
from importlib import import_module
from os.path import abspath
from pathlib import Path
from werkzeug.routing import RequestRedirect
from werkzeug.exceptions import MethodNotAllowed, NotFound
from dotenv import load_dotenv; load_dotenv()
from ..auth import login_manager
# from ..admin import admin
from ..urls import MethodView
from ..conf import get_settings_module
from ..orm.sqla import sql
from ..orm.sqla.migrator import migrate
from ..orm.engine import _generate_engine_uri
# from ..orm.sqla.migrator.engine import _SQLITE_ENGINE, _MYSQL_ENGINE

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

    def _attach_settings_modules(self, settings=None):
        if settings is None: settings = get_settings_module()
        self._add_config(settings)
        self._configure_core_features()
        self._perform_app_registration()


    def _add_config(self, settings) -> None:
        self.settings = settings
        self.import_name = settings.IMPORT_NAME
        self.project_name = settings.PROJECT_NAME
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        self.config["BASE_DIR"] = settings.BASE_DIR
        self.config['SECRET_KEY'] = settings.SECRET_KEY
        self.config['DEBUG'] = settings.DEBUG
        self.debug = settings.DEBUG  
        self.config['SQLALCHEMY_DATABASE_URI'] = _generate_engine_uri(settings.DATABASE)
    
    def _configure_core_features(self):
        # add all the core features of navycut app here.

        self.initIns(sql)
        self.initIns(login_manager)
        # self.initIns(admin)
        migrate.init_app(self, sql)

    def _perform_app_registration(self):
        self._registerApp(self.settings.INSTALLED_APPS)


    def _get_view_function(self, url, method="GET") -> tuple:
        adapter = self.url_map.bind('0.0.0.0')
        try:
            match = adapter.match(url, method=method)
        except RequestRedirect as e:
            # recursively match redirects
            return self._get_view_function(e.new_url, method)
        except (MethodNotAllowed, NotFound):
            # no match
            return None

        try:
            # return the view function and arguments
            return self.view_functions[match[0]], match[1]
        except KeyError:
            # no view is associated with the endpoint
            return None
    
    def _has_view_function(self, url, method="GET") -> bool:
        res = self._get_view_function(url, method)
        
        if res: 
            return True
        
        else: 
            return False

    def _configure_default_index(self):
        
        if self.debug is not False and not self._has_view_function("/"):
            self.add_url_rule(rule="/", view_func=_BaseIndexView.as_view("index"), methods=['GET'])
        
        else: 
            pass
    
    def initIns(self, ins) -> bool:
        ins.init_app(self)
        return True

    def _import_app(self, app:str):
        
        try: 
            app = import_module(app)
        
        except AttributeError: 
            raise AttributeError(f"{app} not installed at {self.config.get('BASE_DIR')}. Dobule check the app name. is it really {app} ?")
        return getattr(app, 'app')

    def _registerApp(self, _appList:list):
        for str_app in _appList: 
            
            try: 
                app = self._import_app(f"{self.project_name}.{str_app}")
            
            except: 
                app = self._import_app(str_app)
            self.register_blueprint(app, url_prefix=app.url_prefix)

    def debugging(self,flag) -> None:
        self.debug = flag
        self.config['DEBUG'] =flag

    def run_wsgi(self, *wargs, **kwargs) -> None:
        self._configure_default_index()
        super(Navycut, self).run(*wargs, **kwargs)

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
        self._name = str(arg_dict['name'])
    
    def add_url_pattern(self, pattern_list:list):
        methods=['GET','PUT', 'DELETE', 'POST', 'HEAD']
        for url_path in pattern_list:
            self.add_url_rule(rule=url_path.url, view_func=url_path.views.as_view(url_path.name), methods=methods)

    def import_app_features(self) -> None:
        import_module(f"{self._name}.models", package=None)
        import_module(f"{self._name}.admin", package=None)

    def register_blueprint(self, *wargs, **kwargs):
        app.register_blueprint(*wargs, **kwargs)

    def __repr__(self):
        return self.import_name


app = Navycut()