from navycut.core import AppSister
from navycut.conf import settings


class UploadServerSister(AppSister):
    seize_power = False
    name = "upload_server"
    static_folder = settings.BASE_DIR / "uploads"
    static_url_path = "/"
    url_prefix = "/static_upload"