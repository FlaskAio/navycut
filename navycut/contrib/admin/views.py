from .site.forms import AdminLoginForm
from ..auth import (login_user, 
                logout_user, 
                authenticate,
                has_group
                )

def admin_login(req, res):
    form = AdminLoginForm()
    
    if form.validate_on_submit():
        user = authenticate(form.username.data, form.password.data)
        
        if user is None: 
            return res.flash("Invalid username or password", 'error')\
                    .redirect("/admin/login")
        
        if not has_group(user, 'super_admin'):
            return res.flash("admin section is only available for super-admin.", 'warning')\
                .redirect("/admin/login/")

        login_user(user)
        return res.redirect('/admin')
    return res.render("admin/_adm_login.html", form=form)


def admin_logout(req, res):
    if req.user.is_authenticated:
        logout_user()
    return res.flash("User logged out successfully", 'success')\
            .redirect("/admin/login")