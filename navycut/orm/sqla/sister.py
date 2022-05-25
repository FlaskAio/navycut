from navycut.core.app_config import AppSister
from .migrator import migrate
from . import sql

#add the db object with migrate object.

migrate.db = sql

class SqlaSister(AppSister):
    seize_power = True
    name="sqla"
    extra_ins = (sql, migrate)
