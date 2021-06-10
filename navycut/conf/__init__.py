from importlib import import_module
from os import environ
from ..errors.server import SettingsFileNotFoundError


def get_settings_module():
    """
    It returns the default settings object, grabbed 
    from the settings file present in project directory.

    for example::

        from navycut.conf import get_settings_module

        settings = get_settings_module()
        print (settings.PROJECT_NAME)
    """
    settings_file = environ.get("NAVYCUT_SETTINGS_MODULE")
    try: return import_module(settings_file)
    except ModuleNotFoundError: raise SettingsFileNotFoundError(settings_file, None)

# settings = get_settings_module()