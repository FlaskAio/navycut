from flask_express._helper import get_main_ctx_view
from ..core._helper_decorators import get_request_ctx_view
import typing as t

if t.TYPE_CHECKING:
    from ..http.request import Request
    from ..http.response import Response

class MiddlewareMixin(object):
    """
    The default middleware mixin class to provide the default
    middleware service for navycut app.
    """
    @staticmethod
    def before_request(req:t.Type["Request"], res:t.Type["Response"]):
        return None
    
    @staticmethod
    def before_first_request(req:t.Type["Request"], res:t.Type["Response"]):
        return None
    
    @staticmethod
    def after_request(req:t.Type["Request"], res:t.Type["Response"]):
        return res

    @staticmethod
    def teardown_request(req:t.Type["Request"], res:t.Type["Response"], exception):
        return exception

    @classmethod
    def __maker__(cls) -> None:
        cls._before_request = get_main_ctx_view(cls.before_request)
        cls._before_first_request = get_main_ctx_view(cls.before_first_request)
        cls._after_request = get_request_ctx_view(cls.after_request)
        cls._teardown_request = get_main_ctx_view(cls.teardown_request)

        return None