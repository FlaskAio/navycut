from navycut.urls import MethodView
from navycut.http import JsonResponse

# write your views here.

class IndexView(MethodView):
    def get(self):
        return JsonResponse(message="Hello World!")

def home(req, res):
    return res.json(dict(name="my name is aniket sarkar!"))
