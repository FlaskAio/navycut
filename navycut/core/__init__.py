""" import default app and default models from here """

from .app_config import Navycut, AppInterface
from ..models import models
from ..admin import NavycutAdmin
# from ..command import command

app = Navycut(__name__, models)
admin = NavycutAdmin(app)
# command.init_app_models(app, models)