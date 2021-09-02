import typing as t

if t.TYPE_CHECKING:
    from navycut import urls

ncUrlPatterns = t.List[t.Union["urls.url", "urls.path", "urls.include"]]

ncUrlPattern = t.Tuple[t.List[t.Union["urls.url", "urls.path", "urls.include"]]]