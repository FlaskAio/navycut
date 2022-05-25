from navycut.urls import path, url, include
from . import views

urlpatterns = [
    # path("" , views.IndexView, "index"),
    url("/", views.homepage, "index"),
    url("/another", views.another_page, "another"),
    url("/aditi", views.aditi, "aditi"),
    url("/mail", views.send_email, "send-email"),
    path("/hello", views.HelloView, "hello-view"),
    url("/blog/<int:id>", views.get_blog, "get_blog"),
    url("/blogger", views.blogger, "blogger"),
]