# from .first_project.config import app, models
from . import settings

from navycut.command import command

settings.app.add_config(settings)

command.init(settings.app, settings.models)

if __name__ == '__main__':
    command.run()