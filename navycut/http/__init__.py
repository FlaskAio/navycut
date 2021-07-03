from flask import (Response as ResponseBase, 
                redirect
                )
from flask.json import dumps
from ..datastructures import NCObject
import typing as t

def JsonResponse(*wargs, **kwargs) -> ResponseBase: 
    """
    Returns the Jsonified object.

    :for example::
    
        from navycut.http import JsonResponse
        class CustomView(MethodView):
            def get(self):
                return JsonResponse(message="Salve Mundi!")
    """
    if len(wargs) and isinstance(wargs[0], NCObject): 
        return ResponseBase(dumps(wargs[0].to_dict()), mimetype='application/json')
    
    return ResponseBase(dumps(wargs[0]), mimetype='application/json') if len(wargs) else ResponseBase(dumps(kwargs), mimetype='application/json')


def HttpResponse(*wargs, **kwargs) -> t.Type[ResponseBase]:
    return ResponseBase(*wargs, **kwargs)

def HTTPRedirect(location:str, 
                code:int, 
                response:t.Optional[t.Type[ResponseBase]]=None
                ) -> t.Type[ResponseBase]:
    """
    Redirect to the specified location.

    :param location:
        the location where you want to redirect.
    :param code:
        the web status code. Default if 302.

    example::

        from navycut.http import HTTPRedirect

        def home(req, res):
            return HTTPRedirect("/admin/login/")
    """
    return redirect(location, code, response)