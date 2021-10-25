from importlib import import_module
from os import environ
import typing as t
from . import global_settings
from ..errors.server import SettingsFileNotFoundError, ImproperlyConfigured
from ..errors.misc import DataTypeMismatchError

__all__ = ("get_settings_module", "settings")

ENVIRONMENT_VARIABLE = "NAVYCUT_SETTINGS_MODULE"

empty = object()


class LazySettings:
    def __init__(self) -> None:
        self.settings_modules = environ.get(ENVIRONMENT_VARIABLE, None)
        if self.settings_modules is None:
            raise SettingsFileNotFoundError
        
        self._wrapped = Settings(self.settings_modules)

    def __getattr__(self, name):
        val = getattr(self._wrapped, name)

        if name == 'SECRET_KEY' and not val:
            raise ImproperlyConfigured("The SECRET_KEY setting must not be empty.")

        self.__dict__[name] = val
        return val

    @property
    def configured(self):
        """Return True if the settings have already been configured."""
        return self._wrapped is not empty

class Settings:
    def __init__(self, settings_module):
        for setting in dir(global_settings):
            if setting.isupper():
                setattr(self, setting, getattr(global_settings, setting))

        self.SETTINGS_MODULE = settings_module

        try: 
            mod = import_module(self.SETTINGS_MODULE)
        
        except:
            raise SettingsFileNotFoundError(self.SETTINGS_MODULE, None)

        tuple_settings = (
            'ALLOWED_HOSTS',
            "INSTALLED_APPS",
        )

        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)

                if (setting in tuple_settings and
                        not isinstance(setting_value, (list, tuple))):
                    raise DataTypeMismatchError(setting_value, "settings file", "list or tuple")

                setattr(self, setting, setting_value)
        
        setattr(self, "SETTINGS_FILE_NAME", self.SETTINGS_MODULE)

settings:t.Type["LazySettings"] = LazySettings()