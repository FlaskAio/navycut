# from flask_restful import  Resource
from flask.views import MethodView as _MethodView
from flask import (request, 
                render_template, 
                render_template_string, 
                abort
                )
from ..errors.misc import DataTypeMismatchError
from ..http.response import Response
from importlib import import_module
from asgiref.sync import async_to_sync
from inspect import iscoroutinefunction as is_async_func
import typing as t
import types as types

class MethodView(_MethodView):
    """
    Navycut default view class to provide the interactive service and features.
    Simply import this class and extend it with your view class.
    for example:: 

        from navycut.urls import MethodView
        from navycut.http import JsonResponse

        class IndexView(MethodView):
            return JsonResponse(message="Salve Mundi!")
        #or
        class IndexView(MethodView):
            return self.render("index.html") # html templates must be present at app's specified template folder.
    """
    # available_methods = []

    def __init__(self, *wargs, **kwargs) -> None:
        super(MethodView, self).__init__(*wargs, **kwargs)

        self.req = self.request = request
        self.res = self.response = Response()
        self.context = dict()


    def get(self, *args, **kwargs):
        """simply override this function for get request"""
        abort(405)

    def put(self, *args, **kwargs):
        """simply override this function for put request"""
        abort(405)

    def post(self, *args, **kwargs):
        """simply override this function for post request"""
        abort(405)

    def delete(self, *args, **kwargs):
        """simply override this function for delete request"""
        abort(405)

    def head(self, *args, **kwargs):
        """simply override this function for head request"""
        abort(405)

    # def option(self, *args, **kwargs):
    #     """simply override this function for option request"""
    #     abort(405)


    def render(self, template_name_or_raw:str, *wargs:tuple, **context:t.Any):
        """
        The function to rend to html templates.
        :param template_name_or_raw:
            single template name or html raw string.
        :param wargs:
            only accept dictionary type value.
        :param context:
            provide the context for the html.

        example::

            class BlogView(MethodView):
                def get(self):
                    blogs = Blog.query.all()
                    return self.render("blog-list.html", blogs=blogs)
        """        
        if len(wargs) and not isinstance(wargs[0], dict): 
            raise DataTypeMismatchError(wargs[0], "template rendering", "dict")
        
        if len(wargs) and isinstance(wargs[0], dict):
            context.update(wargs[0])
        
        if isinstance(template_name_or_raw, str):
            if not template_name_or_raw.endswith(".html") and not template_name_or_raw.endswith(".htm"):
                return render_template_string(template_name_or_raw, **context)
            
            else: 
                return render_template(template_name_or_raw, **context)

    @classmethod
    def as_view(cls, name: str, *class_args: t.Any, **class_kwargs: t.Any):
        """
        create view functions from the source class. 
        It also converts the async functions into sync.
        """
        for method in list(cls.methods):
            if is_async_func(getattr(cls, method.lower())):
                setattr(cls, method.lower(), async_to_sync(getattr(cls, method.lower())))

        return super(MethodView, cls).as_view(name, *class_args, **class_kwargs)


class path:
    """
    create the url_rule map for navycut project using this class.

    :param url_rule:
        the url rule name.
    
    :param views:
        the view class.(Remeber path class takes only class like views.)
    
    :param name:
        the name of the view class. default is views.__name__

    :for example::

        #views.py
        from navycut.urls import MethodView

        class IndexView(MethodView):
            def get(self):
                return "Hello world"
        
        #urls.py
        from navycut.urls import path
        from . import views

        url_patterns = [path("/index", views.IndexView, 'index')]
    """
    def __init__(self, url_rule:str, views, name=None) -> None:
        self.url_rule:str = "/"+url_rule if not url_rule.startswith('/') else url_rule
        self.url_rule = self.url_rule+"/" if not self.url_rule.endswith("/") else self.url_rule
        self.views = views
        self.name:str = name or self.views.__name__
    
    def __repr__(self) -> str:
        """
        return the string representation of the class.
        """
        return f"path <{self.url_rule}>"

class url:
    """
    create the url map for navycut project using this class.

    :param url_rule:
        the url rule name.
    
    :param views:
        the view function.(Remeber url class takes only function like views.)
    
    :param name:
        the name of the view class. default is views.__name__

    :for example::

        #views.py
        def indexview(req, res):
            return res.send("Hello world")
        
        #urls.py
        from navycut.urls import url
        from . import views

        url_patterns = [path("/index", views.indexview, 'index')]
    """
    def __init__(self, url_rule:str, views, name=None) -> None:
        self.url_rule = "/"+url_rule if not url_rule.startswith('/') else url_rule
        self.url_rule = self.url_rule+"/" if not self.url_rule.endswith("/") else self.url_rule
        self.views = views
        self.name = name or self.views.__name__

    def __repr__(self) -> str:
        """
        return the string representation of the class.
        """
        return f"url <{self.url_rule}>"

class include:
    """
    Include the urls from another app using this class.

    :param url_rule:
        the url_rule prefix for the urls present in the imported app.

    :param url_module_name:
        the url module name from where you want to import the urls.

    :for example::

        #urls.py

        #suppose you want to import paths from blog app, 
        # present at your project directory.

        from navycut.urls import include

        url_patterns = [include("/blogs", "blogs.urls")]
    """
    def __init__(self, 
                url_rule:str,
                url_module_name:t.Union[str, types.ModuleType]) -> None:

        self.url_rule = "/"+url_rule if not url_rule.startswith('/') else url_rule
        self.url_rule = self.url_rule[:-1] if self.url_rule.endswith("/") else self.url_rule
        self.url_module = import_module(url_module_name) if isinstance(url_module_name, str) else url_module_name
        self.url_patterns = getattr(self.url_module, "url_patterns")  #self.url_module.url_patterns

        for url_pattern in self.url_patterns:

            url_pattern.url_rule = url_rule+url_pattern.url_rule
            url_pattern.name = url_rule+url_pattern.name

    def __repr__(self) -> str:
        """
        return the string representation of the class.
        """
        return f"include <{self.url_rule}>"