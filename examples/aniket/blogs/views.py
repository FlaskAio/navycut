from navycut.urls import MethodView
from navycut.http import JsonResponse
from navycut.admin.site.auth import login_required
from .models import Blog

# write your views here.

class IndexView(MethodView):
    # @login_required
    def get(self):
        # # blogs = Blog.query.all()
        # blogs = [blog.to_dict() for blog in Blog.all()]
        # return JsonResponse(blogs)
        blog = Blog.query.filter_by(name="this is the first blog").first()
        # print ("Aniket")
        # print (blog.is_exists)
        return blog.to_dict()

    def post(self):
        blog = Blog(name=self.json.name, subject=self.json.subject, body=self.json.body)
        blog.save()
        return JsonResponse(message="done")
