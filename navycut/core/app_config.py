from flask import Flask, Blueprint
from flask_bootstrap import Bootstrap
from importlib import import_module
from werkzeug.routing import RequestRedirect
from werkzeug.exceptions import MethodNotAllowed, NotFound
from ._serving import run_simple_wsgi
from .helper_decorators import _get_req_res_view
from ..errors.misc import (ImportNameNotFoundError, 
                    ConfigurationError,
                    )
from ..urls import MethodView
from ..contrib.mail import mail
from ..http.request import Request
from ..orm.sqla import sql
from ..orm.sqla.migrator import migrate
from ..orm.engine import _generate_engine_uri
from ..utils import path
from ..utils.tools import snake_to_camel_case

import typing as t

if t.TYPE_CHECKING:
    from ..middleware import MiddlewareMixin

_basedir = path.abspath(__file__).parent.parent

class _BaseIndexView(MethodView):
    def get(self):
        return self.render("_index.html")

class Navycut(Flask):

    request_class = Request

    def __init__(self):

        # self.settings = settings

        super(Navycut, self).__init__(__name__, 
                    template_folder=_basedir / 'templates',
                    static_folder=str(_basedir / "static"),
                    static_url_path="/static")

    def _attach_settings_modules(self):
        from ..conf import settings

        self.settings = settings

        self._add_config(settings)
        self._configure_core_features()
        self._perform_app_registration(settings)
        self._perform_middleware_registration(settings)


    def _add_config(self, settings) -> None:
        self.import_name = settings.IMPORT_NAME
        self.project_name = settings.PROJECT_NAME
        self.config['PROJECT_NAME'] = self.project_name
        self.config['IMPORT_NAME'] = self.import_name
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        self.config["BASE_DIR"] = settings.BASE_DIR
        self.config['SECRET_KEY'] = settings.SECRET_KEY
        self.config['SQLALCHEMY_DATABASE_URI'] = _generate_engine_uri(settings.DATABASE)
        self.config['FLASK_ADMIN_FLUID_LAYOUT'] = True
        self.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
        self.config['SETTINGS'] = settings
        self.debugging(settings.DEBUG)

        if settings.EXTRA_ARGS is not None:
            self._add_extra_config(settings)
        
        if settings.MAIL_USING_SMTP:
            self._configure_smtp_mail(settings)

    def _configure_smtp_mail(self, settings):
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

    def _add_extra_config(self, settings) -> None:
        for key, value in settings.EXTRA_ARGS.items():
            self.config[key] = value
    

    def _configure_core_features(self):
        # add all the core features of navycut app here.

        self.initIns(sql)
        self.initIns(mail)
        migrate.init_app(self, sql)
        Bootstrap(self)


    def _perform_app_registration(self, settings):
        """
        attach the available apps on seetings 
        file with the core navycut app.
        """
        self._registerApp(settings.INSTALLED_APPS)

    def _perform_middleware_registration(self, settings):
        """
        attach the available middlewares on 
        settings file with the core navycut app.
        """
        self._registerMiddleware(settings.MIDDLEWARE)

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
        app = app_name
        try: 
            if not app_name.endswith("Sister"):
                _pure_app_name = app_name.rsplit(".", 1)

                if len(_pure_app_name) == 1:
                    _pure_app_name = _pure_app_name[0]
                else:
                    _pure_app_name = _pure_app_name[1]

                app_name = f"{app_name}.sister.{snake_to_camel_case(_pure_app_name)}Sister"
            app_location, app_str_class = tuple(app_name.rsplit(".", 1))
            app_file = import_module(app_location)
            real_app_class = getattr(app_file, app_str_class)
            app = real_app_class()
            if getattr(app, "import_name", None) is None:
                app.import_name = app_file.__name__
            app.init()
        
        except AttributeError: 
            raise AttributeError(f"{app_name} not installed at {self.config.get('BASE_DIR')}. Dobule check the app name. is it really {app} ?")
        return app.get_app()

    def _registerApp(self, _appList:list):
        for str_app in _appList: 
            
            app = self._import_app(str_app)    
            self.register_blueprint(app, url_prefix=app.url_prefix)


    def _import_middleware(self, mw_name:str) -> t.Type["MiddlewareMixin"]:
        mw_file, mw_class_name = tuple(mw_name.rsplit(".", 1))

        mw_module = import_module(mw_file)
        real_mw_class = getattr(mw_module, mw_class_name)

        return real_mw_class


    def _registerMiddleware(self, _mwList:t.List["str"]):
        for middleware in _mwList:
            mw_class = self._import_middleware(middleware)
            mw_maker = getattr(mw_class, "__maker__")

            _before_request, \
                _before_first_request, \
                    _after_request = mw_maker()

            self.before_request(_before_request)

            self.before_first_request(_before_first_request)

            # self.after_request(_after_request) # not working, need to check.


    def debugging(self, flag:bool) -> None:
        self.debug = flag
        self.config['DEBUG'] =flag

    def run_wsgi(self, host:str, port:int, **options) -> None:
        self._configure_default_index()

        addr = f"http://{host}:{port}"

        _run_with_debug = self.config['DEBUG']
        _run_with_reloader = self.config['DEBUG']

        options.setdefault("threaded", True)

        # c.launch(addr) # open the webbrowser containg the provided addr.

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
    """
    The default class to create the 
    helper(side) apps for navycut core app.

    supported params are:
    
    :param import_app_feature:
        type: bool
        Default is False. If True then the app 
        will try to import the default fetaures, i.e admin and models.

    :param url_pattern:
        type: t.Tuple[t.List[t.Union["urls.url", "urls.path", "urls.include"]]]
        add the default url_patterns for the app.
        for example::
            
            from .urls import url_patterns
            class AdminSister(AppSister):
                url_pattern = (url_patterns,)
    """

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
        from navycut.conf import settings
        
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