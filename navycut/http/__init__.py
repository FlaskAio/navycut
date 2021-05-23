from flask import Response
from flask.json import dumps
from ..datastructures import NCObject

def JsonResponse(___=None, **kwargs) -> Response: 
    if ___ is not None and isinstance(___, NCObject): return Response(dumps(___.to_dict()), mimetype='application/json')
    return Response(dumps(___), mimetype='application/json') if ___ is not None else Response(dumps(kwargs), mimetype='application/json')


def HttpResponse(*wargs, **kwargs) -> Response:
    return Response(*wargs, **kwargs)