import os
import typing as t
from pathlib import Path

if t.TYPE_CHECKING:
    from _typeshed import StrPath, BytesPath

def abspath(*wargs):
    """
    returns the absolute PosixPath of then given file object.

    :param file: provide the file name.

    for example::
        
        from navycut.utils import path
        abs_path = path.abspath(__file__)
    """
    return Path(os.path.abspath(*wargs))

def realpath(*wargs):
    """
    returns the real PosixPath of then given file object.

    :param file: provide the file object.

    for example::

        from navycut.utils import path
        abs_path = path.realpath(__file__)
    """
    return Path(os.path.realpath(*wargs))

def exists(path:t.Union[t.AnyStr, t.ByteString]):
    """
    Test weather a path exists. Return False for broken symbloic link.

    :param path:
        String or Bytes like pathname
    """
    
    return os.path.exists(path)

def isDir(path:t.Union[t.AnyStr, t.ByteString]):
    """
    return True is the pathname refers to an existing directory.
    
    :param path:
        String or Bytes like pathname
    """
    return os.path.isdir(path)

def isFile(path:t.Union["StrPath", "BytesPath"]):
    """
    Test whether a path is a regular file
    :param path:
        a str or bytes like filename.
    """
    return os.path.isfile(path)

def join(path:t.Union["StrPath", "BytesPath"], 
            *paths:t.Union["StrPath", "BytesPath"]
            ) -> str:
    """
    Join two or more pathname components, inserting '/' as needed. 
    If any component is an absolute path, all previous 
    path components will be discarded. An empty last part 
    will result in a path that ends with a separator.
    """
    return os.path.join(path, *paths)