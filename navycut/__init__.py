"""
Navycut Project.

Introduction :


"""

__version__ = '1.0.0'
__author__ = "Aniket Sarkar"

def get_version(ctx=None, param=None):
    """
    returns the default version.
    """
    print (__version__)
    return __version__

def get_author():
    """
    returns the default author name.
    """
    return __author__