from flask_login import (LoginManager, 
                    login_required as _login_required)

from flask_login import (LoginManager, 
                    login_user as _login_user)

from flask_login import current_user as _current_user


current_user = _current_user
login_required = _login_required
login_user = _login_user


login_manager = LoginManager()