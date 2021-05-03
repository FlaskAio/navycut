""" import default app and default models from here """

from .app_config import Navycut, SisterApp
from ..orm import db
from ..admin import NavycutAdmin
# from ..command import command

app = Navycut(__name__, db)
admin = NavycutAdmin(app)
# command.init_app_models(app, db)