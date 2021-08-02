"""
Navycut Project.

Introduction :


"""

__version__ = '0.0.3'
__author__ = "Aniket Sarkar"

def get_version(ctx=None, param=None):
    """
    returns the default version.
    """
    return __version__

def get_author():
    """
    returns the default author name.
    """
    return __author__

def setup():
    from .core import app
    """
    setup and provide the default application context service.
    """
    app._attach_settings_modules()
    app_ctx = app.app_context()
    app_ctx.push()