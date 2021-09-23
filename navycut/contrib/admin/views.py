from .site.forms import AdminLoginForm
from ..auth import (
    login_user, 
    logout_user, 
    authenticate,
    has_group
    )
import typing as t

if t.TYPE_CHECKING:
    from navycut.typing.http import ncRequest, ncResponse

async def admin_login(req:"ncRequest", res:"ncResponse"):
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


async def admin_logout(req:"ncRequest", res:"ncResponse"):
    if req.user.is_authenticated:
        logout_user()
    return res.flash("User logged out successfully", 'success')\
            .redirect("/admin/login")