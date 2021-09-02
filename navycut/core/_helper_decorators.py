from inspect import (signature, 
            iscoroutinefunction as is_async_func
            )
from functools import wraps
from ..http.response import Response
from flask.globals import request

from asgiref.sync import async_to_sync as asgiref_async_to_sync

def async_to_sync(func):
    return asgiref_async_to_sync(func)


def get_request_ctx_view(func):
    """
    add only the request object with the view function.
    """
    request_param = signature(func).parameters.get('request', None) \
                            or signature(func).parameters.get('req', None)
    
    is_request:bool = True if request_param is not None else False
    
    if is_async_func(func) is not True:
        wraps(func)
        def decorator(*wargs, **kwargs):
            if is_request is True:
                wargs = list(wargs)
                wargs.insert(0, request)
                wargs = tuple(wargs)
            return func(*wargs, **kwargs)
        return decorator
    
    else:
        wraps(func)
        async def decorator(*wargs, **kwargs):
            if is_request is True:
                wargs = list(wargs)
                wargs.insert(0, request)
                wargs = tuple(wargs)
            return await func(*wargs, **kwargs)
        return decorator

def get_response_ctx_view(func):
    """
    add only the response object with the view function.
    """
    response_param = signature(func).parameters.get('response', None) \
                            or signature(func).parameters.get('res', None)
    
    is_response = True if response_param is not None else False
    
    if is_async_func(func) is not True:
        wraps(func)
        def decorator(*wargs, **kwargs):
            if is_response is True:
                wargs = list(wargs)
                wargs.insert(0, Response())
                wargs = tuple(wargs)

            return func(*wargs, **kwargs)
        
        return decorator
    
    else:
        wraps(func)
        async def decorator(*wargs, **kwargs):
            if is_response is True:
                wargs = list(wargs)
                wargs.insert(0, Response())
                wargs = tuple(wargs)

            return await func(*wargs, **kwargs)
        
        return decorator