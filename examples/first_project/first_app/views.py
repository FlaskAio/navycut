from navycut.urls import ModelView
from navycut.http import JsonResponse

class IndexView(ModelView):
    def get(Self):
        return JsonResponse(message="Salve Mundi!")