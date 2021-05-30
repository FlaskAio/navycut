from navycut.core import SisterApp
from navycut.conf import get_settings_module

settings = get_settings_module()

config_dict = dict(
        import_name = __name__,
        name = "static_server",
        static_folder =  settings.BASE_DIR / "uploads",
        static_url_path = "/",
        url_prefix = "/static_upload",
        template_folder = None,
)

app = SisterApp(config_dict)