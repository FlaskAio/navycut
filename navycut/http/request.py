from flask.wrappers import Request as RequestBase
from flask.globals import request

from flask_login import current_user


class Request(RequestBase):

    def __init__(self, *wargs, **kwargs) -> None:
        super(Request, self).__init__(*wargs, **kwargs)

    @property
    def user(self):
        return current_user