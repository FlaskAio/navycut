from flask_mailman.backends.smtp import EmailBackend as _EmailBackend

class EmailBackend(_EmailBackend):
    """
    The default smtp backend.
    Actually we are using flask_mailman 
    module's backend class here.
    """