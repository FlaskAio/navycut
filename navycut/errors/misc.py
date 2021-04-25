
class DataTypeMismatchError(Exception):
    def __init__(self, data, place:str=None, required_data_type:str=None) -> None:
        message = f"{data} datatype isn't supported for {place}.\nRequired datatype is: {required_data_type}, got: {str(type(data))}"
        super(DataTypeMismatchError, self).__init__(message)

class InsufficientArgumentsError(Exception):
    def __init__(self, message):
        message = f"Insufficient arguments.\n{message}"
        super(InsufficientArgumentsError, self).__init__(message)

class DirectoryAlreadyExistsError(Exception):
    def __init__(self,project_dir):
        message = f"{project_dir} already exists at the location."
        super(DirectoryAlreadyExistsError, self).__init__(message)