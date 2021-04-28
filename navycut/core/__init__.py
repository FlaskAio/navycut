""" import default app and default models from here """

from .app_config import Navykut, SisterApp
from ..models import models
from ..admin import NavykutAdmin
# from ..command import command

app = Navykut(__name__, models)
admin = NavykutAdmin(app)
# command.init_app_models(app, models)