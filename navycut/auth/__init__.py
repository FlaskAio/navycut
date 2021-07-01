from flask_login import (LoginManager, 
                    login_required as _login_required,
                    login_user as _login_user,
                    current_user as _current_user
                    )
from flask import (abort, 
                current_app)
from functools import wraps


current_user = _current_user

def login_required(*wargs, **kwargs):
    return _login_required(*wargs, **kwargs)

def login_user(*wargs, **kwargs):
    return _login_user(*wargs, **kwargs)


login_manager = LoginManager()


def group_required(*groups_name):
    def decorated_function(f):
        @wraps(f)

        def wrapper_func(*wargs, **kwargs):

            if current_user.is_authenticated:

                for group in current_user.groups:
                    if group.name in groups_name:
                        return f(*wargs, **kwargs)

                abort(401)
            
            else:
                return current_app.login_manager.unauthorized()
        
        return wrapper_func
    
    return decorated_function