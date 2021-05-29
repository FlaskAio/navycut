if __name__ == '__main__':
    from navycut.command import manage_command
    from os import environ
    environ.setdefault('NAVYCUT_SETTINGS_MODULE', 'test2.settings')
    manage_command()