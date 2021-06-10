from flask import Flask, Blueprint
from importlib import import_module
from os.path import abspath
from pathlib import Path
from werkzeug.routing import RequestRedirect
from werkzeug.exceptions import MethodNotAllowed, NotFound
from dotenv import load_dotenv; load_dotenv()
from ..errors.misc import ImportNameNotFoundError
from ..auth import login_manager
from ..urls import MethodView
from ..conf import get_settings_module
from ..orm.sqla import sql
from ..orm.sqla.migrator import migrate
from ..orm.engine import _generate_engine_uri

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

    def _import_app(self, app_name:str):
        
        try: 
            app_location, app_str_class = tuple(app_name.rsplit(".", 1))
            app_file = import_module(app_location)
            real_app_class = getattr(app_file, app_str_class)
            print ("app_name:", app_file.__name__)
            app = real_app_class()
            if getattr(app, "import_name") is None:
                app.import_name = app_file.__name__
            try: 
                app.init()
            except:
                pass
        
        except AttributeError: 
            raise AttributeError(f"{app_name} not installed at {self.config.get('BASE_DIR')}. Dobule check the app name. is it really {app} ?")
        return app.get_app()

    def _registerApp(self, _appList:list):
        for str_app in _appList: 
            
            try: 
                app = self._import_app(str_app)    
            
            except: 
                app = self._import_app(f"{self.project_name}.{str_app}")

            self.register_blueprint(app, url_prefix=app.url_prefix)

    def debugging(self,flag) -> None:
        self.debug = flag
        self.config['DEBUG'] =flag

    def run_wsgi(self, *wargs, **kwargs) -> None:
        self._configure_default_index()
        super(Navycut, self).run(*wargs, **kwargs)

    def __repr__(self):
        return self.import_name

class AppSister:

    import_app_feature:bool = False

    extra_url_pattern:tuple = None

    import_name:str = None

    name:str = None

    template_folder = None

    static_folder = None

    static_url_path = None

    url_prefix = None
    
    extra_ins:tuple = None
    
    def init(self, **kwargs) -> None:

        if self.import_name is None:
            raise ImportNameNotFoundError("app_register")

        if self.name is None:
            self.name = "_".join(self.import_name.split("."))

        if isinstance(self.import_name, tuple):
            self.import_name = self.import_name[0]

        if isinstance(self.template_folder, tuple):
            self.template_folder = self.template_folder[0]

        if isinstance(self.static_folder, tuple):
            self.static_folder = self.static_folder[0]

        if isinstance(self.static_url_path, tuple):
            self.static_url_path = self.static_url_path[0]

        if isinstance(self.url_prefix, tuple):
            self.url_prefix = self.url_prefix[0]

        if isinstance(self.import_app_feature, tuple):
            self.import_app_feature = self.import_app_feature[0]

        # if isinstance(self.extra_url_pattern, tuple):
        #     self.extra_url_pattern = self.extra_url_pattern[0]


        if self.template_folder is not None:
            kwargs.update(dict(template_folder=self.template_folder,))

        if self.static_folder is not None:
            kwargs.update(dict(static_folder=self.static_folder,))

        if self.static_url_path is not None:
            kwargs.update(dict(static_url_path=self.static_url_path,))

        if self.url_prefix is not None:
            kwargs.update(dict(url_prefix=self.url_prefix,))
                

        # The default blueprint object for each sister app
        self.power = Blueprint(self.name, self.import_name, **kwargs)

        if self.extra_ins is not None:
            for ins in self.extra_ins:
                ins.init_app(app)

        if self.extra_url_pattern is not None:
            for url_pattern in self.extra_url_pattern:
                self.add_url_pattern(url_pattern)

        if self.import_app_feature is True:
            self.import_app_features()


    def get_app(self):
        return self.power
        
    def init_while_registration(self, import_name, **kwargs):
        self.import_name = import_name
        self.name = kwargs.pop('name', None)
        self.init(**kwargs)

    def add_url_pattern(self, pattern_list:list):
        methods=['GET','PUT', 'DELETE', 'POST', 'HEAD']
        for url_path in pattern_list:
            self.power.add_url_rule(rule=url_path.url, view_func=url_path.views.as_view(url_path.name), methods=methods)

    def import_app_features(self) -> None:
        """
        To use this feature you must need to set the 
        value of name variable same as the app name, 
        otherwise it may not work properly.
        """
        import_module(f"{self.name}.models", package=None)
        import_module(f"{self.name}.admin", package=None)

    def register_blueprint(self, *wargs, **kwargs):
        app.register_blueprint(*wargs, **kwargs)

    def __repr__(self):
        return self.import_name


app = Navycut()