from . import MiddlewareMixin
from ..conf import settings
import typing as t

if t.TYPE_CHECKING:
    from ..http.request import Request
    from ..http.response import Response


class IPFilterMiddleware(MiddlewareMixin):
    """
    The default middleware class to prevent 
    the access from unwanted IP address.

    `ALLOWED_HOST` setting is required for this middleware.
    """

    def before_request(req:t.Type["Request"], res:t.Type["Response"]):
        allowed_host:t.List[str] = settings.ALLOWED_HOST
        
        if len(allowed_host) == 1 and allowed_host[0] == "*":
            return None
        
        else:
            if req.remote_addr not in allowed_host:
                return res.end(403)