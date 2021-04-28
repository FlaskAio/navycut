# from flask_restful import  Resource
from flask.views import MethodView as _MethodView
from flask import request, render_template, render_template_string
from ..errors.misc import DataTypeMismatchError
# from flask_restful import Api as _Api

class MethodView(_MethodView):
    def __init__(self, *wargs, **kwargs) -> None:
        super(MethodView, self).__init__(*wargs, **kwargs)
        self.request = request
    
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

def path(url, views, name=None):
    if not url.startswith('/'): url += "/"
    name = name or views.__name__
    return (url, views, name)