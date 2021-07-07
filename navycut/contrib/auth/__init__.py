from flask_login import (LoginManager, 
                    login_required as _login_required,
                    login_user as _login_user,
                    logout_user as _logout_user,
                    current_user
                    )
from flask import (abort, 
                current_app
                )
from functools import wraps
import typing as t
from ..admin.site.models import User
from navycut.utils.security import check_password_hash
from navycut.errors.misc import DataTypeMismatchError

if t.TYPE_CHECKING:
    from datetime import timedelta


login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id) -> t.Type["User"]:
    return User.query.get(int(user_id))



def login_required(func):
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

def login_user(user:t.Type["User"], 
            remember:bool=False, 
            duration:t.Optional[t.Type["timedelta"]]=None, 
            force:bool=False, 
            fresh:bool=True
            ) -> bool:
    """
    Logs a user in. You should pass the actual user object to this. If the
    user's `is_active` property is ``False``, they will not be logged in
    unless `force` is ``True``.

    This will return ``True`` if the log in attempt succeeds, and ``False`` if
    it fails (i.e. because the user is inactive).

    :param user: The user object to log in.
    :type user: object
    :param remember: Whether to remember the user after their session expires.
        Defaults to ``False``.
    :type remember: bool
    :param duration: The amount of time before the remember cookie expires. If
        ``None`` the value set in the settings is used. Defaults to ``None``.
    :type duration: :class:`datetime.timedelta`
    :param force: If the user is inactive, setting this to ``True`` will log
        them in regardless. Defaults to ``False``.
    :type force: bool
    :param fresh: setting this to ``False`` will log in the user with a session
        marked as not "fresh". Defaults to ``True``.
    :type fresh: bool
    """
    return _login_user(user, remember=False, duration=None, force=False, fresh=True)

def logout_user() -> bool:
    """
    Logs a user out. (You do not need to pass the actual user.) 
    This will also clean up the remember me cookie if it exists.
    """
    return _logout_user()


def group_required(*groups_name):
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

def has_group(user: t.Type["User"], 
            group:t.Union[t.List[str], str]
            ) -> bool:
    """
    check a user have the provided group or not.
    :param user:
        the user object.
    :param group:
        the group you want to check.
    example::

        from navycut.contrib.auth import has_group
        from navycut.contrib.admin.site.models import user
        user = User.query.get(1)
        is_group_present = has_group(user, 'super_admin')
    """
    user_groups_name = [group.name for group in list(user.groups)]  
    if isinstance(group, str):
        return group in user_groups_name  
    
    elif isinstance(group, list):
        for grp in group:
            if grp in user_groups_name:
                return True
        return False

    else:
        raise DataTypeMismatchError(type(group).__name__, "has_group function", "str or list")