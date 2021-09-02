from flask.ctx import has_request_context
from flask_express.request import Request as RequestBase
from flask.globals import ( 
                    current_app, 
                    _request_ctx_stack
                    ) 
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