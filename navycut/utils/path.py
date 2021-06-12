from os import path
from pathlib import Path


def abspath(*wargs):
    """
    returns the absolute PosixPath of then given file object.

    :param file: provide the file name.

    for example::
        from navycut.utils import path
        abs_path = path.abspath(__file__)
    """
    return Path(path.abspath(*wargs))

def realpath(*wargs):
    """
    returns the real PosixPath of then given file object.

    :param file: provide the file object.

    for example::
        from navycut.utils import path
        abs_path = path.realpath(__file__)
    """
    return Path(path.realpath(*wargs))