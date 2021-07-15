from navycut.core import app
from functools import wraps

def with_appcontext(f):
    @wraps(f)
    def decorated_function(*wargs, **kwargs):
        with app.app_context():
            return f(*wargs, **kwargs)
    return decorated_function