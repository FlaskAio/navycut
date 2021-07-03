from .site.forms import AdminLoginForm
from flask import flash
from .site.models import User
from ..utils.security import check_password_hash
from ..auth import login_user, logout_user

def admin_login(req, res):
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user: 
            flash("Invalid username")
            return res.redirect("/admin/login")
            
        if not check_password_hash(user.password, form.password.data): 
            flash ("Invalid password")
            return res.redirect("/admin/login")

        login_user(user)
        return res.redirect('/admin')
    return res.render("admin/_adm_login.html", form=form)


def admin_logout(req, res):
    if req.user.is_authenticated:
        logout_user()
    flash("User logged out successfully")
    return res.redirect("/admin/login")