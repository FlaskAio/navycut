from flask import json
from json.decoder import JSONDecodeError
from flask.wrappers import Response as ResponseBase
from flask.templating import (render_template, 
                    render_template_string
                    )
from ..errors.misc import (DataTypeMismatchError, 
                    InsufficientArgumentsError, 
                    InvalidArgumentsError,
                    NCBaseError
                    )
import typing as t
from werkzeug.exceptions import *


STATUS_DICT:dict = {
            400 : Unauthorized,
            403 : Forbidden,
            404 : NotFound,
            405 : MethodNotAllowed,
            406 : NotAcceptable,
            408 : RequestTimeout,
            409 : Conflict,
            410 : Gone,
            411 : LengthRequired,
            412 : PreconditionFailed,
            413 : RequestEntityTooLarge,
            414 : RequestURITooLarge,
            415 : UnsupportedMediaType,
            416 : RequestedRangeNotSatisfiable,
            417 : ExpectationFailed,
            418 : ImATeapot,
            422 : UnprocessableEntity,
            423 : Locked,
            424 : FailedDependency,
            428 : PreconditionRequired,
            429 : TooManyRequests,
            431 : RequestHeaderFieldsTooLarge,
            451 : UnavailableForLegalReasons,
            500 : InternalServerError,
            501 : NotImplemented,
            502 : BadGateway,
            503 : ServiceUnavailable,
            504 : GatewayTimeout,
            505 : HTTPVersionNotSupported
}


class Response(ResponseBase):


    @classmethod
    def send(cls, content:t.Union[str, dict, t.List[t.Any]]) -> t.Type[ResponseBase]:
        
        if isinstance(content, dict) or isinstance(content, list):
            return cls.json(content)

        if hasattr(content, 'to_dict'):
            return cls.json(content.to_dict())

        try:
            _ = json.loads(content)
            return cls.json(content)

        except JSONDecodeError:
            return cls(content)

        except Exception as e:
            raise NCBaseError(e)

    @classmethod
    def json(cls, *wargs:t.Any, **kwargs:t.Any) -> ResponseBase:
        
        data:str = json.dumps(dict())
        
        if len(wargs):
            try:
                data:str = json.dumps(wargs[0])
            
            except TypeError:
                if hasattr(wargs[0], 'to_dict'):
                    data:str = json.dumps(wargs[0].to_dict())
                
                else:
                    raise DataTypeMismatchError(wargs[0], "response class", "dict or list")
            
            except Exception as e:
                raise NCBaseError(e)

        else:
            if kwargs is not None:
                data:str = json.dumps(kwargs)

        return cls(data, mimetype="application/json", status=200)

    @classmethod
    def end(cls, code:int=None):
        if code is not None:
            cls.set_status(code)

        else:
            return cls("")

    @classmethod
    def set_status(cls, code:int) -> None:
        if not code in STATUS_DICT:
            raise InvalidArgumentsError(f"{code} is the invalid web status code.")
        else:
            raise STATUS_DICT.get(code)

    @classmethod
    def render(cls, *wargs:t.Any, **context:t.Any):

        if not len(wargs):
            raise InsufficientArgumentsError("atleast 1 argument is required for render method.")

        if len(wargs) > 1 and not isinstance(wargs[1], dict): 
            raise DataTypeMismatchError(wargs[1], "template rendering", "dict")
        
        if len(wargs) > 1 and isinstance(wargs[1], dict):
            context.update(wargs[1])
        
        if isinstance(wargs[0], str):
            if not wargs[0].endswith(".html") and not wargs[0].endswith(".htm"):
                return render_template_string(wargs[0], **context)
            
            else: 
                return render_template(wargs[0], **context)