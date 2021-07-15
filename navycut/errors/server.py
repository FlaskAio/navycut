class SettingsFileNotFoundError(Exception):
    def __init__(self, filename:str=None, location:str=None) -> None:
        if (filename and location) is None:
            message = "settings file not found. Please define the environment variable 'NAVYCUT_SETTINGS_MODULE' to use settings."

        else:
            message = f"{filename}.py file not found at {location}"
        
        super(SettingsFileNotFoundError, self).__init__(message)

class ImproperlyConfigured(Exception):
    def __init__(self, *args: object) -> None:
        super(ImproperlyConfigured, self).__init__(*args)