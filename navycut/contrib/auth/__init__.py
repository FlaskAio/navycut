from flask_login import (
    LoginManager as _LoginManager, 
    logout_user as _logout_user,
    login_user as _login_user
    )
from .models import User
from navycut.utils.security import check_password_hash
from navycut.errors.misc import DataTypeMismatchError

from .decorators import (
    login_required as login_required, 
    group_required as group_required,
    )

import typing as t

if t.TYPE_CHECKING:
    from navycut.core.app_config import Navycut
    from datetime import timedelta
    from .models import User


class LoginManager(_LoginManager):
    def __init__(self, 
                app:t.Type["Navycut"]=None, 
                add_context_processor:bool=True
                ) -> None:

        
        super(LoginManager, self).__init__(app=app, 
                                add_context_processor=add_context_processor)
        # self. login_view = "/login/"


login_manager = _LoginManager()

@login_manager.user_loader
def load_user(user_id) -> t.Type["User"]:
    return User.query.get(int(user_id))

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
    return _login_user(user, remember=remember, duration=duration, force=force, fresh=fresh)


def logout_user() -> bool:
    """
    Logs a user out. (You do not need to pass the actual user.) 
    This will also clean up the remember me cookie if it exists.
    """
    return _logout_user()


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
        from navycut.contrib.auth.models import user
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
        raise DataTypeMismatchError(group, "has_group function", "str or list")