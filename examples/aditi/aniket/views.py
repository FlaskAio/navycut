# from flask.wrappers import Request
from navycut.contrib.auth import login_required
# from .models import Blog, Author

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

def get_blog(req, res, id):
    # author = Author.query.get(id)
    blog =Blog.query.get(id)
    print (blog.author)
    return res.json(blog.author)