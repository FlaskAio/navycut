from flask_login import (LoginManager, 
                    login_required as _login_required,
                    login_user as _login_user,
                    logout_user as _logout_user,
                    current_user as _current_user
                    )
from flask import (abort, 
                current_app)
from functools import wraps
import typing as t
from ..admin.site.models import User
from navycut.utils.security import check_password_hash


current_user = _current_user

def login_required(*wargs, **kwargs):
    return _login_required(*wargs, **kwargs)

def login_user(*wargs, **kwargs):
    return _login_user(*wargs, **kwargs)

def logout_user(*wargs, **kwargs):
    return _logout_user(*wargs, **kwargs)


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

@login_manager.user_loader
def load_user(user_id) -> t.Type["User"]:
    return User.query.get(int(user_id))

def authenticate(username:str, password:str) -> t.Optional["User"]:
    """
    The default authentication method to authenticate a user in Navycut.

    :param username:
        The username for authentication.
    :param password:
        the original password for the given user.

    example::

        from navycut.auth import authenticate
        user = authenticate(username="jhon", password="password")

    """

    user = User.query.filter_by(username=username).first()
    if not user is None:
        if not check_password_hash(user.password, password):
            return None
    return user