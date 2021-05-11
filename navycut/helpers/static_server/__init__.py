from navycut.core import SisterApp
from navycut.conf import get_settings_module

settings = get_settings_module()

config_dict = dict(
        import_name = "static_server",
        name = __name__,
        static_folder =  settings.BASE_DIR / "uploads",
        static_url_path = "/",
        url_prefix = "/static_server",
        template_folder = None,
)

app = SisterApp(config_dict)