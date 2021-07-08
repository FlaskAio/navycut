from flask import json, redirect, flash
from json.decoder import JSONDecodeError
from flask.wrappers import Response as ResponseBase
from flask.templating import (render_template, 
                    render_template_string
                    )
from ..errors.misc import (DataTypeMismatchError, 
                    InsufficientArgumentsError, 
                    NCBaseError
                    )
import typing as t
from werkzeug.exceptions import *
from sqlalchemy.orm.collections import InstrumentedList


ERROR_DICT:dict = {
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
            505 : HTTPVersionNotSupported,
}


class Response:
    def __init__(self):
        self.status_code = 200

    def flash(self, message:str, category:str="info") -> t.Type["Response"]:
        flash(message, category=category)
        return self

    def send(self, content:t.Union[str, dict, t.List[t.Any]]) -> t.Type[ResponseBase]:
        
        if isinstance(content, dict) or isinstance(content, list):
            return self.json(content)

        if hasattr(content, 'to_dict'):
            return self.json(content.to_dict())

        try:
            _ = json.loads(content)
            return self.json(content)

        except JSONDecodeError:
            return ResponseBase(content, status_code=self.status_code)

        except Exception as e:
            raise NCBaseError(e)

    def json(self, *wargs:t.Any, **kwargs:t.Any) -> ResponseBase:
        
        data:str = json.dumps(dict())
        
        if len(wargs):
            try:
                data:str = json.dumps(wargs[0])
            
            except TypeError:
                if isinstance(wargs[0], InstrumentedList):
                    _res_list:list = [d.to_dict() for d in wargs[0]]
                    data = json.dumps(_res_list)

                elif hasattr(wargs[0], 'to_dict'):
                    data:str = json.dumps(wargs[0].to_dict())
                
                else:
                    raise DataTypeMismatchError(wargs[0], "response class", "dict or list")
            
            except Exception as e:
                raise NCBaseError(e)

        else:
            if kwargs is not None:
                data:str = json.dumps(kwargs)

        return ResponseBase(data, mimetype="application/json", status=self.status_code)

    def end(self, code:int=None):
        if code is not None:
            self.status(code)

        else:
            return ResponseBase("", status=self.status_code)

    def status(self, code:int) -> t.Optional["Response"]:
        
        if code in ERROR_DICT:
            raise ERROR_DICT.get(code)
        
        else:
            self.status_code = code
            return self

    def render(self, *wargs:t.Any, **context:t.Any) -> t.Type[str]:

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

    def redirect(self, route):
        return redirect(route)