from flask import Response
from flask.json import dumps
from ..datastructures import NCObject

def JsonResponse(*wargs, **kwargs) -> Response: 
    """
    Returns the Jsonified object.
    :for example::
        from navycut.http import JsonResponse
        class CustomView(MethodView):
            def get(self):
                return JsonResponse(message="Salve Mundi!")
    """
    if len(wargs) and isinstance(wargs[0], NCObject): 
        return Response(dumps(wargs[0].to_dict()), mimetype='application/json')
    
    return Response(dumps(wargs[0]), mimetype='application/json') if len(wargs) else Response(dumps(kwargs), mimetype='application/json')


def HttpResponse(*wargs, **kwargs) -> Response:
    return Response(*wargs, **kwargs)