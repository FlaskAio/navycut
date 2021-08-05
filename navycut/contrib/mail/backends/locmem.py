from flask_mailman.backends.locmem import EmailBackend as _EmailBackend

class EmailBackend(_EmailBackend):
    """
    The default local memory backend.
    Actually we are using flask_mailman 
    module's backend class here.
    """