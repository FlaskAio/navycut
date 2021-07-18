from inspect import signature
from functools import wraps
from ..http.response import Response
from flask.globals import request


def _get_main_ctx_view(f):
    """
    adding the default request, response object with view function
    """
    request_param = signature(f).parameters.get('request', None) \
                            or signature(f).parameters.get('req', None)
    
    is_request = True if request_param is not None else False

    response_param = signature(f).parameters.get('response', None) \
                            or signature(f).parameters.get('res', None)
    
    is_response = True if response_param is not None else False

    @wraps(f)
    def decorator(*args, **kwargs):
        if is_request is True:

            args:list = list(args)
            args.insert(0, request)

        if is_response is True:
            args:list = list(args)
            if len(args):
                args.insert(1, Response())
            else:
                args.insert(0, Response())
        
        args:tuple = tuple(args)
        return f(*args, **kwargs)
    return decorator


def _get_request_ctx_view(f):
    request_param = signature(f).parameters.get('request', None) \
                            or signature(f).parameters.get('req', None)
    
    is_request = True if request_param is not None else False
    
    wraps(f)
    def decorator(*wargs, **kwargs):
        if is_request is True:
            wargs = list(wargs)
            wargs.insert(0, request)
            wargs = tuple(wargs)

        return f(*wargs, **kwargs)
    
    return decorator

def _get_response_ctx_view(f):
    response_param = signature(f).parameters.get('response', None) \
                            or signature(f).parameters.get('res', None)
    
    is_response = True if response_param is not None else False
    
    wraps(f)
    def decorator(*wargs, **kwargs):
        if is_response is True:
            wargs = list(wargs)
            wargs.insert(0, Response())
            wargs = tuple(wargs)

        return f(*wargs, **kwargs)
    
    return decorator