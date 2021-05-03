from dip import settings

from navycut.command import Command

settings.app.addConfig(settings)

command = Command(settings)

if __name__ == '__main__':
    command.run()
