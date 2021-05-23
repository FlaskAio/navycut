from navycut.urls import MethodView
from navycut.http import JsonResponse, HttpResponse

# write your views here.

class IndexView(MethodView):
    def get(self):
        return HttpResponse("Salve Mundi!")
        # return JsonResponse(message="Salve Mundi!")
