# from .first_project.config import app, models

from aa import app, models
from navycut.command import command

# settings.app.addConfig(settings)

command.init(app, models)

if __name__ == '__main__':
    command.run()
