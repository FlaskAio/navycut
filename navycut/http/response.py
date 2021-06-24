# from flask import json
from flask import json
from json.decoder import JSONDecodeError
from flask.wrappers import Response as ResponseBase
from flask.templating import (render_template, 
                    render_template_string
                    )
import typing as t
from ..errors.misc import DataTypeMismatchError


class Response(ResponseBase):


    @classmethod
    def send(cls, content:t.Union[str, dict, t.List[t.Any]]):
        
        if isinstance(content, dict) or isinstance(content, list):
            content = json.dumps(content)
            return cls(content, mimetype="application/json")

        try:
            _ = json.loads(content)
            return cls(content, mimetype="application/json")

        except JSONDecodeError:
            return cls(content)

        except Exception:
            raise Exception

    @classmethod
    def json(cls, *wargs:t.Any, **kwargs:t.Any) -> ResponseBase:
        
        data:str = json.dumps(dict())
        
        if len(wargs):
            try:
                data:str = json.dumps(wargs[0])
            except Exception as e:
                raise DataTypeMismatchError(wargs[0], "response class", "dict or list")

        else:
            if kwargs is not None:
                data:str = json.dumps(kwargs)

        return cls(data, mimetype="application/json")

    @classmethod
    def end(cls):
        return cls("")

    # @classmethod
    # def status(cls, code:int):
    #     return cls(status=code)

    @classmethod
    def render(cls, template_name_or_raw:str, *wargs:t.Any, **context:t.Any):
        if len(wargs) and not isinstance(wargs[0], dict): 
            raise DataTypeMismatchError(wargs[0], "template rendering", "dict")
        
        if len(wargs) and isinstance(wargs[0], dict):
            context.update(wargs[0])
        
        if isinstance(template_name_or_raw, str):
            if not template_name_or_raw.endswith(".html") and not template_name_or_raw.endswith(".htm"):
                return render_template_string(template_name_or_raw, **context)
            
            else: 
                return render_template(template_name_or_raw, **context)