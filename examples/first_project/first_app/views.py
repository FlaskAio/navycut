from navykut.urls import ModelView
from navykut.http import JsonResponse

class IndexView(ModelView):
    def get(Self):
        return JsonResponse(message="Salve Mundi!")