class SettingsFileNotFoundError(Exception):
    def __init__(self, filename, location) -> None:
        message = f"{filename}.py file not found at {location}"
        super(SettingsFileNotFoundError, self).__init__(message)