from flask_mailman.backends.console import EmailBackend as _EmailBackend

class EmailBackend(_EmailBackend):
    """
    The default console backend.
    Actually we are using flask_mailman 
    module's backend class here.
    """