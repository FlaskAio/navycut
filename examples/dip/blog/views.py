from navycut.urls import MethodView
from navycut.http import JsonResponse
from .models import *

# write your views here.

class IndexView(MethodView):
    def get(self):
        return JsonResponse(message="Salve Mundi!")

class GargiView(MethodView):
    def get(self):
        gargi= Gargi.query.get(1)
        return JsonResponse(gargi.to_dict())
    def post(self):
        gargi = Gargi(name=self.json.name, subject=self.json.subject, body=self.json.body)
        gargi.save()
        return gargi.to_dict()