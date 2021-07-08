class NCBaseError(Exception):
    def __init__(self, message) -> None:
        super(NCBaseError, self).__init__(message)


class DataTypeMismatchError(Exception):
    def __init__(self, provided_data, place:str=None, required_data_type:str=None) -> None:
        message = f"{provided_data} datatype isn't supported for {place}.\nRequired datatype is: {required_data_type}, got: {str(type(provided_data).__name__)}"
        super(DataTypeMismatchError, self).__init__(message)

class InsufficientArgumentsError(Exception):
    def __init__(self, message):
        message = f"Insufficient arguments.\n{message}"
        super(InsufficientArgumentsError, self).__init__(message)

class InvalidArgumentsError(Exception):
    def __init__(self, message:str) -> None:
        super(InvalidArgumentsError, self).__init__(message)

class DirectoryAlreadyExistsError(Exception):
    def __init__(self,project_dir):
        message = f"{project_dir} already exists at the location."
        super(DirectoryAlreadyExistsError, self).__init__(message)

class ImportNameNotFoundError(Exception):
    def __init__(self, location) -> None:
        message = f"import_name notm provided for the sister app at {location}"
        super(ImportNameNotFoundError, self).__init__(message)

class ConfigurationError(Exception):
    def __init__(self, message) -> None:
        super(ConfigurationError, self).__init__(message)