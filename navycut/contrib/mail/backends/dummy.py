from flask_mailman.backends.dummy import EmailBackend as _EmailBackend

class EmailBackend(_EmailBackend):
    """
    The default dummy backend.
    Actually we are using flask_mailman 
    module's backend class here.
    """