"""
Do not change anything if you dont have enough knowledge 
how to handle it, otherwise it may mess the server.
"""

from navycut.core import AppSister
from navycut.utils import path


__basedir__ = path.abspath(__file__).parent


class AniketSister(AppSister):
    name = "aniket"
    template_folder = __basedir__ / "templates"
    static_folder = __basedir__ / "static"
    static_url_path = "/static"
    url_prefix = "/aniket"
    import_app_feature = True