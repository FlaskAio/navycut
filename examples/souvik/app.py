from navycut.core import app
from importlib import import_module

settings = import_module("souvik.settings")

app._attach_settings_modules(settings)