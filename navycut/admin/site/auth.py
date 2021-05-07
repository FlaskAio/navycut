from flask.globals import current_app
from flask_login import LoginManager 
from flask_login import LoginManager, login_required as _login_required
from flask_login import LoginManager, login_user as _login_user
from flask_login import current_user as _current_user
from flask import current_app as _current_app
# from flask import current_app
from .models import User

# app = current_app
current_app = _current_app
current_user = _current_user
login_required = _login_required
login_user = _login_user

# class AuthManager:
#     def __init__(self, App):pass
#         # global app
#         # app = App
    
# # if app is not None:
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))