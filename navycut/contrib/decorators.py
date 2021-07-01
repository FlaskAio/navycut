from inspect import signature
from ..http.response import Response
from flask.globals import request

def _get_req_res_view(f):
        """
        adding the default request object with view function
        """

        request_param = signature(f).parameters.get('request', None) \
                                or signature(f).parameters.get('req', None)
        
        is_request = True if request_param is not None else False

        response_param = signature(f).parameters.get('response', None) \
                                or signature(f).parameters.get('res', None)
        
        is_response = True if response_param is not None else False

        def decorator(*args, **kwargs):
            if is_request is True:

                args:list = list(args)
                args.insert(0, request)

            if is_response is True:
                args:list = list(args)
                if len(args):
                    args.insert(1, Response)
                else:
                    args.insert(0, Response)
           
            args:tuple = tuple(args)
            return f(*args, **kwargs)
        return decorator