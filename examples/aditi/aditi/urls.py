from navycut.contrib.admin import urls as admin_urls
from navycut.urls import include

urlpatterns = [
    include("/admin/", admin_urls),
    include("/aniket", "aniket.urls")
]