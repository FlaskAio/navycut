# from .first_project.config import app, models
from . import settings

from navykut.command import command

settings.app.addConfig(settings)

command.init(settings.app, settings.models)

if __name__ == '__main__':
    command.run()