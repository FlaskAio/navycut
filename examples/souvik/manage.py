if __name__ == '__main__':
    from navycut.command import Command
    from os import environ
    environ.setdefault('NAVYCUT_SETTINGS_MODULE', 'souvik.settings')
    command = Command()
    command.run()