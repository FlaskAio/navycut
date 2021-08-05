from flask_mailman.backends.filebased import EmailBackend as _EmailBackend

class EmailBackend(_EmailBackend):
    """
    The default filebased backend.
    Actually we are using flask_mailman 
    module's backend class here.
    """