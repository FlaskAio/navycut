from importlib import import_module
from os import environ
from ..errors.server import SettingsFileNotFoundError
from ..errors.misc import NCBaseError

__all__ = ("get_settings_module", "settings")

"""
import the default settings file module 
from the project directory.

:for example::

    from navycut.conf import settings
    print (settings.PROJECT_NAME)
"""

def get_settings_module():
    """
    It returns the default settings object, grabbed 
    from the settings file present in project directory.

    for example::

        from navycut.conf import get_settings_module
        settings = get_settings_module()
        print (settings.PROJECT_NAME)
    
    another example::

        from navycut.conf import settings
        print (settings.PROJECT_NAME)
    """
    settings_file = environ.get("NAVYCUT_SETTINGS_MODULE")

    try: 
        settings = import_module(settings_file)
        setattr(settings, "SETTINGS_FILE_NAME", environ.get("NAVYCUT_SETTINGS_MODULE"))
        return settings

    except ModuleNotFoundError: 
        raise SettingsFileNotFoundError(settings_file, None)

    except Exception as e:
        raise NCBaseError(e)

settings = get_settings_module()