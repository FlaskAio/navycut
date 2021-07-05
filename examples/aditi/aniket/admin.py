from navycut.contrib import admin
from .models import *

admin.register_model(Blog)
admin.register_model(Author)
admin.register_model(ExtraUser)