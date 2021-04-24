from flask import Response
from flask.json import dumps

def JsonResponse(___=None, **____) -> Response: return Response(dumps(___), mimetype='application/json') if ___ is not None else Response(dumps(____), mimetype='application/json')