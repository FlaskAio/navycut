from werkzeug.exceptions import abort
from navycut.middleware import MiddlewareMixin
import typing as t
from flask import redirect
from flask_login import current_user

if t.TYPE_CHECKING:
    from navycut.http.request import Request
    from navycut.http.response import Response


class AdminAuthMiddleware(MiddlewareMixin):

    def before_request(req:t.Type["Request"], res:t.Type["Response"]):
        if "/admin/" in req.url \
            and not req.blueprint == "navycut_contrib_admin_sister" \
                and not "/static/admin/" in req.url:

            if not req.user.is_authenticated is True:
                return res.flash("login is required")\
                    .redirect("/admin/login/")
