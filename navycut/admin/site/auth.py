from flask_login import LoginManager, current_user, login_required, login_user
# from flask import current_app
from .models import User

# app = current_app

current_user = current_user
login_required = login_required
login_user = login_user

# class AuthManager:
#     def __init__(self, App):pass
#         # global app
#         # app = App
    
# # if app is not None:
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))