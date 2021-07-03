# from flask.wrappers import Request
from navycut.auth import login_required, group_required
from navycut.admin.site.models import User

def homepage(req, res):
    return res.json(dict(req.headers))

# @login_required
# @group_required("super_admin")
def another_page(req, res):
    # r = Request(request.environ)
    # print (req.user.username)
    # return res.status(201).json(name=req.user.name)
    # return res.end()
    return res \
        .status(200)\
        .render("<h1>Hello {{name}}</h1>", name="Aniket")

@login_required
def aditi(req, res):
    return res.json(username=req.user.username)