from navycut.core import AppSister
from navycut.conf import settings


class UploadServerSister(AppSister):
    static_folder = settings.BASE_DIR / "uploads",
    static_url_path = "/",
    url_prefix = "/static_upload"