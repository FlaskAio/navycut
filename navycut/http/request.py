from flask.wrappers import Request as RequestBase
from ..datastructures._object import NCObject

from ..contrib.auth import current_user


class Request(RequestBase):

    def __init__(self, *wargs, **kwargs) -> None:
        super(Request, self).__init__(*wargs, **kwargs)

    @property
    def user(self):
        return current_user

    @property
    def json(self):
        return NCObject(self.get_json())

    @property
    def query(self):
        return NCObject(self.args)

    @property
    def body(self):
        return NCObject(self.form)