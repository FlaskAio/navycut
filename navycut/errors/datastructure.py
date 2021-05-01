class NCObjectDataTypeMisMatchError(Exception):
    def __init__(self, provided_data):
        message = f"NCObject only receives json or dictionary data type, not {type(provided_data).__name__}"
        super(NCObjectDataTypeMisMatchError, self).__init__(message)
