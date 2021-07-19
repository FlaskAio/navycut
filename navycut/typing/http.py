import typing as t


if t.TYPE_CHECKING:
    from ..http.response import Response
    from ..http.request import Request


ncRequest = t.Type["Request"]
ncResponse = t.Type["Response"]