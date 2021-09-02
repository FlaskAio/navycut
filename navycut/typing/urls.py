import typing as t

if t.TYPE_CHECKING:
    from navycut import urls

urlPatterns = t.List[t.Union["urls.url", "urls.path", "urls.include"]]

urlPattern = t.Tuple[t.List[t.Union["urls.url", "urls.path", "urls.include"]]]