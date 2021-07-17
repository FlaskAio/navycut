from flask_login import ( login_required as _login_required,
                    current_user
                    )
from flask import (abort, 
                current_app
                )
from functools import wraps
import typing as t


def login_required(func) -> t.Any:
    """
    If you decorate a view with this, it will ensure that the current user is
    logged in and authenticated before calling the actual view. (If they are
    not, it calls the :attr:`LoginManager.unauthorized` callback.) For
    example::

        @login_required
        def post(req, res):
            pass

    If there are only certain times you need to require that your user is
    logged in, you can do so with::

        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()

    ...which is essentially the code that this function adds to your views.

    It can be convenient to globally turn off authentication when unit testing.
    To enable this, if the application configuration variable `LOGIN_DISABLED`
    is set to `True`, this decorator will be ignored.

    .. Note ::

        Per `W3 guidelines for CORS preflight requests
        <http://www.w3.org/TR/cors/#cross-origin-request-with-preflight-0>`_,
        HTTP ``OPTIONS`` requests are exempt from login checks.

    :param func: The view function to decorate.
    :type func: function
    """
    return _login_required(func)


def group_required(*groups_name) -> t.Any:
    """
    If you decorate a view with this, it will ensure that the 
    current user is under the provided group names before 
    calling the actual view. 
    (If they arenot, it calls the :attr:`LoginManager.unauthorized` callback.) 
    For example::

        @group_required("super_admin", "admin")
        def post(req, res):
            pass

    If the current user dosen't belong from the provided groups, it will 
    throw the 400 Unauthorized error.
    """
    def decorated_function(f):
        @wraps(f)

        def wrapper_func(*wargs, **kwargs):

            if current_user.is_authenticated:

                for group in current_user.groups:
                    if group.name in groups_name:
                        return f(*wargs, **kwargs)

                abort(400)
            
            else:
                return current_app.login_manager.unauthorized()
        
        return wrapper_func
    
    return decorated_function