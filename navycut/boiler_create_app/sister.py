"""
Do not change anything if you dont have enough knowledge 
how to handle it, otherwise it may mess the server.
"""

from navycut.core import AppSister
from navycut.utils import path
from .urls import urlpatterns


__basedir__ = path.abspath(__file__).parent


class classname___boiler_var(AppSister):
    name = "import_name___boiler_var"
    template_folder = __basedir__ / "templates"
    static_folder = __basedir__ / "static"
    static_url_path = "/static"
    url_prefix = "/import_name___boiler_var"
    url_pattern = (urlpatterns, )
    import_app_feature = True