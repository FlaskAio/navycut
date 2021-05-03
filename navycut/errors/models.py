class ModelsIntegrityError(Exception):
    def __init__(self, e):
        _dict = e.__dict__
        message = f"Failed to create UNIQUE constraint.\nLocation: {str(_dict.get('orig')).split(':')[1].strip()}\nparams: {str(_dict.get('params'))}"
        super(ModelsIntegrityError, self).__init__(message)