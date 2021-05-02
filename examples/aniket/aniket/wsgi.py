from . import settings

settings.app.addConfig(settings)
settings.app.debugging(False)

application = settings.app
