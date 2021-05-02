from navycut.urls import MethodView
from navycut.http import JsonResponse
from navycut.admin.site.auth import login_required

# write your views here.

class IndexView(MethodView):
    @login_required
    def get(self):
        print (self.request.blueprint)
        return JsonResponse(self.query)

    def post(self):
        return JsonResponse(self.json)
