if __name__ == '__main__':
    from navycut.command import Command
    from os import environ
    environ.setdefault('NAVYCUT_SETTINGS_MODULE', 'kalyanj.settings')
    command = Command()
    command.run()