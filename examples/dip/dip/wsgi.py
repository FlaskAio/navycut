from . import settings

settings.app.add_config(settings)
settings.app.debugging(False)

application = settings.app
