import os
import typing as t
from pathlib import Path


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

def isdir(path:t.Union[t.AnyStr, t.ByteString]):
    """
    return True is the pathname refers to an existing directory.
    
    :param path:
        String or Bytes like pathname
    """
    return os.path.isdir(path)