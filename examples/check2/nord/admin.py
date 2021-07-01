from navycut.admin import admin
from .models import *

admin.register_model(AniketSarkar, category=str(__name__).split(".")[0].capitalize())