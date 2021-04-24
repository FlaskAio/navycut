# from .first_project.config import app, models
try: from .first_project import settings
except: from first_project import settings

from navycut.command import command

settings.app.addConfig(settings)

command.init(settings.app, settings.models)

if __name__ == '__main__':
    command.run()