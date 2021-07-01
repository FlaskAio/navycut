from flask import Flask, Blueprint
from importlib import import_module
from werkzeug.routing import RequestRedirect
from werkzeug.exceptions import MethodNotAllowed, NotFound
from ._serving import run_simple_wsgi
from ..errors.misc import (ImportNameNotFoundError, 
                    ConfigurationError
                    )
from ..auth import login_manager
from ..urls import MethodView
from ..conf import settings
from ..contrib.mail import mail
from ..http.request import Request
from ..contrib.decorators import _get_req_res_view
from ..orm.sqla import sql
from ..orm.sqla.migrator import migrate
from ..orm.engine import _generate_engine_uri
from ..utils import path

_basedir = path.abspath(__file__).parent.parent

class _BaseIndexView(MethodView):
    def get(self):
        return self.render("_index.html")

class Navycut(Flask):

    request_class = Request

    def __init__(self):

        self.settings = settings

        super(Navycut, self).__init__(settings.IMPORT_NAME, 
                    template_folder=_basedir / 'templates',
                    static_folder=str(_basedir / "static"),
                    static_url_path="/static")

    def _attach_settings_modules(self):
        self._add_config()
        self._configure_core_features()
        self._perform_app_registration()


    def _add_config(self) -> None:
        self.import_name = settings.IMPORT_NAME
        self.project_name = settings.PROJECT_NAME
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        self.config["BASE_DIR"] = settings.BASE_DIR
        self.config['SECRET_KEY'] = settings.SECRET_KEY
        self.debugging(settings.DEBUG)
        self.config['SQLALCHEMY_DATABASE_URI'] = _generate_engine_uri(settings.DATABASE)
        
        if settings.MAIL_USING_SMTP:
            self._configure_smtp_mail()

    def _configure_smtp_mail(self):
        """
        The default config function to take smtp creds 
        from settings file and attach with the navycut app.
        """
            
        if settings.SMTP_CONFIGURATION.get("is_using_tls") == settings.SMTP_CONFIGURATION.get("is_using_ssl"):
            raise ConfigurationError("the value of 'is_using_ssl' and 'is_using_tls' can't be same at a time for SMTP.")
        
        for key, value in settings.SMTP_CONFIGURATION.items():
            
            if value is None:
                raise ConfigurationError(f"The value for {key} in SMTP CONFIGURATION can't be None, \
                    \nwhile the MAIL_USING_SMTP settings is true.")

        self.config['MAIL_SERVER'] = settings.SMTP_CONFIGURATION.get("host", None)
        self.config['MAIL_PORT'] = settings.SMTP_CONFIGURATION.get("port", None)
        self.config['MAIL_USE_TLS'] = settings.SMTP_CONFIGURATION.get("is_using_tls", None)
        self.config['MAIL_USE_SSL'] = settings.SMTP_CONFIGURATION.get("is_using_ssl", None)
        self.config['MAIL_USERNAME'] = settings.SMTP_CONFIGURATION.get("username", None)
        self.config['MAIL_PASSWORD'] = settings.SMTP_CONFIGURATION.get("password", None)
    

    def _configure_core_features(self):
        # add all the core features of navycut app here.

        self.initIns(sql)
        self.initIns(login_manager)
        self.initIns(mail)

        migrate.init_app(self, sql)


    def _perform_app_registration(self):
        self._registerApp(settings.INSTALLED_APPS)


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

    def debugging(self, flag:bool) -> None:
        self.debug = flag
        self.config['DEBUG'] =flag
        if flag is True:
            self.config['ENV'] = 'development'

        else:
            self.config['ENV'] = 'production'

    def run_wsgi(self, host, port, **options) -> None:
        self._configure_default_index()

        _run_with_debug = self.config['DEBUG']
        _run_with_reloader = self.config['DEBUG']

        options.setdefault("threaded", True)

        run_simple_wsgi(host, 
                        port, 
                        self, 
                        _run_with_reloader, 
                        _run_with_debug, 
                        **options
                        )

    def __repr__(self) -> str:
        return self.import_name

class AppSister:

    import_app_feature:bool = False

    url_pattern:tuple = None

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

        if self.template_folder is not None:
            kwargs.update(dict(template_folder=self.template_folder,))
        else:
            kwargs.update(dict(template_folder=settings.TEMPLATE_DIR))

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
                app.initIns(ins)

        if self.url_pattern is not None:
            for url_pattern in self.url_pattern:
                self.add_url_pattern(url_pattern)

        if self.import_app_feature is True:
            self.import_app_features()


    def get_app(self) -> Blueprint:
        return self.power     

    def add_url_pattern(self, pattern_list:list) -> None:

        methods=['GET','PUT', 'DELETE', 'POST', 'HEAD', 'OPTIONS']

        for url_path in pattern_list:
            if repr(url_path).startswith("path"):
                self.power.add_url_rule(rule=url_path.url, view_func=url_path.views.as_view(url_path.name), methods=methods)
            
            elif repr(url_path).startswith("url"):
                view_func = _get_req_res_view(url_path.views)
                self.power.add_url_rule(rule=url_path.url, endpoint= url_path.name, view_func=view_func, methods=methods)
            
            elif repr(url_path).startswith("include"):
                self.add_url_pattern(url_path.url_patterns)
            
            else:
                pass

    
    def import_app_features(self) -> None:
        """
        To use this feature you must need to set the 
        value of name variable same as the app name, 
        otherwise it may not work properly.
        """
        import_module(f"{self.name}.models", package=None)
        import_module(f"{self.name}.admin", package=None)

    def register_blueprint(self, *wargs, **kwargs) -> None:
        app.register_blueprint(*wargs, **kwargs)

    def __repr__(self):
        return self.import_name


app:Navycut = Navycut()