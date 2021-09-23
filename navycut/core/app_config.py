from flask import Blueprint
from flask_express import FlaskExpress
from flask_bootstrap import Bootstrap

from importlib import import_module
from werkzeug.routing import RequestRedirect
from werkzeug.exceptions import MethodNotAllowed, NotFound

from ._serving import run_simple_wsgi
from ..http.request import Request
from ..http.response import Response
from ..errors.misc import ImportNameNotFoundError
from ..urls import MethodView
from ..utils import path
from ..utils.tools import snake_to_camel_case

import typing as t

if t.TYPE_CHECKING:
    from ..middleware import MiddlewareMixin
    from .. import urls

_basedir = path.abspath(__file__).parent.parent

class _BaseIndexView(MethodView):
    """
    The default index view for a navycut project.
    """
    def get(self):
        return self.render("_index.html")

class Navycut(FlaskExpress):
    """
    The base class of navycut project.
    It's basically inheritaing the services from the class Flask.

    We have customized some the core flask features 
    to provide this huge and fullstack service.
    """

    request_class = Request
    response_class = Response

    def __init__(self):
        super(Navycut, self).__init__("app_default_name", 
                    template_folder=_basedir / 'templates',
                    static_folder=str(_basedir / "static"),
                    static_url_path="/static")

    def _attach_settings_modules(self):
        """
        attach all the available and required
        settings features with the core app.
        """
        from ..conf import settings

        self.settings = settings

        self._add_config(settings)
        self._configure_core_features()
        self._perform_sister_registration(settings)
        self._perform_middleware_registration(settings)


    def _add_config(self, settings) -> None:
        """
        add teh required and default 
        configuration with the core app.

        :param settings:
            the settings object from the project directory.
        """
        self.import_name = settings.IMPORT_NAME
        self.project_name = settings.PROJECT_NAME
        self.config['PROJECT_NAME'] = settings.PROJECT_NAME
        self.config['IMPORT_NAME'] = settings.IMPORT_NAME
        self.config["BASE_DIR"] = settings.BASE_DIR
        self.config['SECRET_KEY'] = settings.SECRET_KEY
        self.config['FLASK_ADMIN_FLUID_LAYOUT'] = True
        self.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
        self.config['SETTINGS'] = settings

        self._configure_database(settings)
        self._configure_default_mailer(settings)
        self.debugging(settings.DEBUG)

        if settings.EXTRA_ARGS is not None:
            self._add_extra_config(settings)
        

    def _configure_database(self, settings) -> bool:
        """
        configure the default database as per the 
        details provided from settings.py `DATABASE`

        :param settings:
            the default settings object from the project directory.
        """
        db_engine_name:str = settings.DATABASE['engine']

        db_engine_file_name, db_engine_type = db_engine_name.rsplit(".", 1)
        db_engine_module:t.ModuleType = import_module(db_engine_file_name)

        db_engineer:t.Callable[["Navycut", t.Dict[str, str]], None] 

        db_engineer = getattr(db_engine_module, db_engine_type)

        db_engineer(self, settings.DATABASE["creds"])

        return True

    def _configure_default_mailer(self, settings):
        """
        The default config function to take smtp creds 
        from settings file and attach with the navycut app.

        :param settings:
            the settings object from the project directory.
        """
        self.config['MAIL_SERVER'] = settings.EMAIL_HOST
        self.config['MAIL_PORT'] = settings.EMAIL_PORT
        self.config['MAIL_USE_TLS'] = settings.EMAIL_USE_TLS
        self.config['MAIL_USE_SSL'] = settings.EMAIL_USE_SSL
        self.config['MAIL_USERNAME'] = settings.EMAIL_HOST_USER
        self.config['MAIL_PASSWORD'] = settings.EMAIL_HOST_PASSWORD
        self.config['MAIL_TIMEOUT'] = settings.EMAIL_TIMEOUT
        self.config['MAIL_SSL_KEYFILE'] = settings.EMAIL_SSL_KEYFILE
        self.config['MAIL_SSL_CERTFILE'] = settings.EMAIL_SSL_CERTFILE
        self.config['MAIL_DEFAULT_SENDER'] = settings.DEFAULT_FROM_EMAIL
        self.config['MAIL_BACKEND'] = settings.EMAIL_BACKEND
        self.config['MAIL_FILE_PATH'] = settings.EMAIL_FILE_PATH
        self.config['MAIL_USE_LOCALTIME'] = settings.EMAIL_USE_LOCALTIME
        self.config['MAIL_DEFAULT_CHARSET'] = settings.EMAIL_DEFAULT_CHARSET

    def _add_extra_config(self, settings) -> None:
        """
        config the extra settings provided 
        from settings.py - `EXTRA_ARGS`.

        :param settings:
            the settings object from the project directory.
        """
        for key, value in settings.EXTRA_ARGS.items():
            self.config[key] = value
    

    def _configure_core_features(self):
        """
        add all the core features of navycut app here.
        """
        Bootstrap(self)


    def _perform_sister_registration(self, settings):
        """
        attach the available apps on seetings 
        file with the core navycut app.

        :param settings:
            the settings object from the project directory.
        """
        self._registerSister(settings.INSTALLED_APPS)

    def _perform_middleware_registration(self, settings):
        """
        attach the available middlewares on 
        settings file with the core navycut app.

        :param settings:
            the settings object from the project directory.
        """
        self._registerMiddleware(settings.MIDDLEWARE)

    def _get_view_function(self, url, method="GET") -> tuple:
        """
        get the view function for a particulat url.

        :param url:
            the url whose view function you want to find out.

        :param method:
            the request method. default is `GET`
        """
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
        """
        check wheather a view fucntion is 
        present or not for the provided url.

        :param url:
            the url whose view function you want to check i.e present or not.

        :param method:
            the request method. default is `GET`
        """
        res = self._get_view_function(url, method)
        
        if res: 
            return True
        
        else: 
            return False

    def _configure_default_index(self):
        """
        If the project directory dosen't contain the view 
        for the index page and teh debug is in true mode, 
        then navycut will show a default index page 
        with the help of this function.
        """
        
        if self.debug is not False and not self._has_view_function("/"):
            self.add_url_rule(rule="/", view_func=_BaseIndexView.as_view("index"), methods=['GET'])
        
        else: 
            pass
    
    def initIns(self, ins) -> bool:
        """
        initialize the extra instances with the core app.
        :param ins:
            extra instance object.
        """
        ins.init_app(self)
        return True

    def _import_sister(self, sister_name:str):
        """
        import the app by app_name.

        :param app_name:
            string type full name fo the app.
        """ 
        try: 
            if not sister_name.endswith("Sister"):
                _pure_sister_name = sister_name.rsplit(".", 1)

                if len(_pure_sister_name) == 1:
                    _pure_sister_name = _pure_sister_name[0]
                else:
                    _pure_sister_name = _pure_sister_name[1]

                sister_name = f"{sister_name}.sister.{snake_to_camel_case(_pure_sister_name)}Sister"
            sister_location, sister_class_name = tuple(sister_name.rsplit(".", 1))
            sister_file = import_module(sister_location)
            real_sister_class = getattr(sister_file, sister_class_name)
            sister = real_sister_class()

            if getattr(sister, "import_name", None) is None:
                sister.import_name = sister_file.__name__

            return sister

        except AttributeError: 
            raise AttributeError(f"{sister_name} not installed at {self.config.get('BASE_DIR')}. Dobule check the app name. is it really {sister_name} ?")

    def _registerSister(self, _sisters:list):
        """
        register all the sister apps present in the settings.py - `INSTALLED_APPS`.

        :param _sisters:
            the list containing the name of the apps.
        """
        for str_sister in _sisters: 
            sister:t.Type["AppSister"] = self._import_sister(str_sister)  
            sister.init() #init the core features of the sister app.
            sister_power:t.Type["Blueprint"] = sister.get_sister_power()
            if sister_power is not None:
                self.register_blueprint(sister_power, url_prefix=sister_power.url_prefix)


    def _import_middleware(self, mw_name:str) -> t.Type["MiddlewareMixin"]:
        """
        import the middleware by middleware name.

        :param mw_name:
            teh str name of teh middleware, want to import.
        """
        mw_file, mw_class_name = tuple(mw_name.rsplit(".", 1))

        mw_module = import_module(mw_file)
        real_mw_class = getattr(mw_module, mw_class_name)

        return real_mw_class


    def _registerMiddleware(self, _mwList:t.List["str"]):
        """
        register all the middlewares present at settings.py - `MIDDLEWARE`.

        :param _mwList:
            the list containing the name of the middlewares.
        """
        for middleware in _mwList:
            mw_class:t.Type["MiddlewareMixin"] = self._import_middleware(middleware)
            mw_maker = getattr(mw_class, "__maker__")

            mw_maker() # attach the request, response object with the middleware function.

            self.before_first_request_funcs\
                    .append(mw_class._before_first_request)
                    
            self.after_request_funcs\
                .setdefault(None, [])\
                    .append(mw_class._after_request)

            self.before_request_funcs\
                .setdefault(None, [])\
                    .append(mw_class._before_request)

            self.teardown_request_funcs\
                .setdefault(None, [])\
                    .append(mw_class._teardown_request)



    def debugging(self, flag:bool) -> None:
        """
        to change the debugging mode of the core app 
        then please play with this function.

        make it `False` for production use.

        :param flag:
            your desired state of the app's debug feature.
        """
        self.debug = flag
        self.config['DEBUG'] =flag

    def run(self, host:str="0.0.0.0", port:int=8888, **options) -> None:
        return self.run_wsgi(host, port, **options)

    def run_wsgi(self, host:str, port:int, **options) -> None:
        """
        run the default wsgi server.

        :param host:
            the default hostname to run the interactive server.

        :param port:
            the default port number to run the interactive server.

        :param options:
            other kwargs type vaule to provide more 
            options to the werkzeug run_simple server.
        """
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
        """
        The representation of the Navycut class.
        """
        return self.import_name

class AppSister:
    """
    The default class to create the 
    sister(side) app for navycut core app.

    supported params are:
    
    :param import_app_feature:
    :type bool:
        Default is False. If True then the app 
        will try to import the default fetaures, i.e admin and models.

    :param url_pattern:
    :type t.Optional[t.Tuple[t.List[t.Union["urls.url", "urls.path", "urls.include"]]]]:
        add the default url_patterns for the app.

    :param import_name:
    :type t.Optional[str]:
        the import_name parameter for the sister's blueprint object.

    :param name:
    :type t.Optional[str]:
        the name parameter for the sister's blueprint object. 
        This is required if you turn the `import_app_feature` to True.

    :param template_folder:
    :type t.Optional[str]:
        define the template folder for the sister app.

    :param static_folder:
    :type t.Optional[str]:
        define the static folder for the sister app.

    :param static_url_path:
    :type t.Optional[str]:
        define the url path for the static files.

    :param url_prefix:
    :type t.Optional[str]:
        url_prefix for all the routes of a sister app.

    :param extra_ins:
    :type t.Optional[t.Tuple[object]]:
        provide extra instances to init with main navycut app.

    :param seize_power:
    :type bool:
        default is False, if True then the sister app will 
        not create any blueprint object. Please turn it to 
        True if you don't want to add any url patterns with your sister app.

    :for example::

        from navycut.core import AppSister
        from .urls import url_patterns

        class CustomSister(AppSister):
            import_name = __name__
            name = "custom"
            url_pattern = (url_patterns, )
            ...
    """

    import_app_feature:bool = False

    url_pattern:t.Optional[t.Tuple[t.List[t.Union["urls.url", "urls.path", "urls.include"]]]] = None

    import_name: t.Optional[str] = None

    name: t.Optional[str] = None

    template_folder: t.Optional[str] = None

    static_folder: t.Optional[str] = None

    static_url_path: t.Optional[str] = None

    url_prefix: t.Optional[str] = None
    
    extra_ins:t.Optional[t.Tuple[object]] = None

    seize_power:bool = False
    
    def init(self, **kwargs) -> None:
        """
        start initializing the sister app features.
        """
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

        if isinstance(self.seize_power, tuple):
            self.seize_power = self.seize_power[0]

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


        if self.extra_ins is not None:
            for ins in self.extra_ins:
                app.initIns(ins)


        if self.import_app_feature is True:
            self.import_app_features()

        # The default blueprint object for each sister app
        self.power:t.Optional["Blueprint"] = self._create_power_object(**kwargs)


    def _create_power_object(self, **kwargs) -> t.Optional["Blueprint"]:
        if self.seize_power is not True:
            power = Blueprint(self.name, self.import_name, **kwargs)

            if self.url_pattern is not None:
                for up in self.url_pattern:
                    self.add_url_pattern(power, up)

            return power
        
        else:
            return None

    def get_sister_power(self) -> t.Optional[Blueprint]:
        """
        return the default blueprint 
        object(power) for the selected sister app.
        """
        return self.power     

    def add_url_pattern(self, power:t.Type["Blueprint"], pattern_list:list) -> None:
        """
        add the url pattern with the blueprint power object.

        :param pattern_list:
            the url_pattern list.
        """

        methods=['GET','PUT', 'DELETE', 'POST', 'HEAD', 'OPTIONS']

        for url_path in pattern_list:
            if repr(url_path).startswith("path"):
                power.add_url_rule(rule=url_path.url_rule, view_func=url_path.views.as_view(url_path.name), methods=methods)
            
            elif repr(url_path).startswith("url"):
                view_func = url_path.views
                power.add_url_rule(rule=url_path.url_rule, endpoint= url_path.name, view_func=view_func, methods=methods)
            
            elif repr(url_path).startswith("include"):
                self.add_url_pattern(power, url_path.url_patterns)
            
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
        """
        register extra blueprints with the coer app.
        """
        app.register_blueprint(*wargs, **kwargs)

    def __repr__(self):
        """
        the representation of the AppSister class
        """
        return f"<AppSister '{self.name}'>"



"""
create the default navycut app here.
"""
app:Navycut = Navycut()