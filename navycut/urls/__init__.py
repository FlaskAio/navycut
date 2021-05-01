# from flask_restful import  Resource
from flask.views import MethodView as _MethodView
from flask import request, render_template, render_template_string, session
from ..errors.misc import DataTypeMismatchError
from flask import abort
from ..datastructures import NCObject
# from flask_restful import Api as _Api

class MethodView(_MethodView):
    """
    Navycut default view class to provide the interactive service and features.
    Simply import this class and extend it eith your view class.example: 

    from navycut.urls import MethodView
    from navycut.http import JsonResponse

    class IndexView(MethodView):
        return JsonResponse(message="Salve Mundi!")
    """
    def __init__(self, *wargs, **kwargs) -> None:
        super(MethodView, self).__init__(*wargs, **kwargs)
        self.request = request
        # self.session = NCObject(dict(session))
    
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
    def query(self) -> dict:
        return self.request.args
    
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