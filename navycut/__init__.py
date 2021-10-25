"""
Navycut Project.

Introduction :


"""
version_info = (0, 0, 5)


__version__ = ".".join([str(v) for v in version_info])
__author__ = "Aniket Sarkar"

def get_version():
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