# from flask_restful import  Resource
from flask.views import MethodView as _MethodView
from flask import (request, 
                render_template, 
                render_template_string, 
                session, 
                Request)
from ..errors.misc import DataTypeMismatchError
from flask import abort
from ..datastructures import NCObject
# from flask import current_app, Flask
# from flask_restful import Api as _Api

# class _Request(Request):
# here I can use the current_app features.
#     def __init__(self):
#         super(_Request, self).__init__(current_app.config)

class MethodView(_MethodView):
    """
    Navycut default view class to provide the interactive service and features.
    Simply import this class and extend it with your view class.
    example: 

    from navycut.urls import MethodView
    from navycut.http import JsonResponse

    class IndexView(MethodView):
        return JsonResponse(message="Salve Mundi!")
    #or
    class IndexView(MethodView):
        return self.render("index.html") # html templates must be present at app's specified template folder.
    """
    def __init__(self, *wargs, **kwargs) -> None:
        super(MethodView, self).__init__(*wargs, **kwargs)

        self.request = request
        # self.session = NCObject(dict(session))
   
    # @Request.application
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

    @property
    def query(self) -> NCObject:
        """It returns the url query as NCObject format."""
        return NCObject(self.request.args)
    
    @property
    def json(self):
        return NCObject(self.request.get_json())

    
    @property
    def session(self) -> None:
        return session

    def render(self, template_one_or_list_or_str, ___:dict=None, **context):
        context = context
        if ___ is not None and not isinstance(___, dict): raise DataTypeMismatchError(___, "template rendering", "dict")
        if ___ is not None and isinstance( ___, dict):
            context.update(___)
        if isinstance(template_one_or_list_or_str, str):
            if not template_one_or_list_or_str.endswith(".html") and not template_one_or_list_or_str.endswith(".htm"):
                return render_template_string(template_one_or_list_or_str, **context)
            else: return render_template(template_one_or_list_or_str, **context)


class path:
    def __init__(self, url:str, views, name=None):
        self.url = "/"+url if not url.startswith('/') else url
        self.views = views
        self.name = name or self.views.__name__