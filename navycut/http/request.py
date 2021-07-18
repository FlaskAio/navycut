from flask.ctx import has_request_context
from flask.wrappers import Request as RequestBase
from flask.globals import (session, 
                    current_app, 
                    _request_ctx_stack
                    ) 
from ..datastructures._object import NCObject
from werkzeug.local import LocalProxy
import typing as t

if t.TYPE_CHECKING:
    from ..contrib.auth.models import User


def _get_user():
    if has_request_context() and not hasattr(_request_ctx_stack.top, 'user'):
        current_app.login_manager._load_user()

    return getattr(_request_ctx_stack.top, 'user', None)

class Request(RequestBase):

    def __init__(self, *wargs, **kwargs) -> None:
        super(Request, self).__init__(*wargs, **kwargs)

    @property
    def user(self) -> t.Type["User"]:
        return LocalProxy(lambda: _get_user())

    @property
    def json(self) ->t.Type[NCObject]:
        return NCObject(self.get_json())

    @property
    def query(self) ->t.Type[NCObject]:
        return NCObject(self.args)

    @property
    def body(self) ->t.Type[NCObject]:
        return NCObject(self.form)

    @property
    def session():
        return session