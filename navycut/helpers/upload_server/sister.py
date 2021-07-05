from navycut.core import AppSister
from navycut.conf import get_settings_module

settings = get_settings_module()


class UploadServerSister(AppSister):
    static_folder = settings.BASE_DIR / "uploads",
    static_url_path = "/",
    url_prefix = "/static_upload"

# app = AppSister(import_name=__name__,
#                 name="upload_server",
#                 static_folder=settings.BASE_DIR / "uploads",
#                 static_url_path = "/",
#                 url_prefix = "/static_upload",
#                 )