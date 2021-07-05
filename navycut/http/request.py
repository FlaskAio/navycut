from flask.wrappers import Request as RequestBase
from flask.globals import session
from ..datastructures._object import NCObject

from ..contrib.auth import current_user
import typing as t


class Request(RequestBase):

    def __init__(self, *wargs, **kwargs) -> None:
        super(Request, self).__init__(*wargs, **kwargs)

    @property
    def user(self):
        return current_user

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