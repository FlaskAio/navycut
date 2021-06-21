from navycut.urls import MethodView
from navycut.http import JsonResponse
from .form import RegistrationForm

# write your views here.

class IndexView(MethodView):
    def get(self):
        return JsonResponse(message="Salve Mundi!")

class AuthView(MethodView):
    def get(self):
        form = RegistrationForm(self.request.form)
        return self.render('register.html', form=form)
        
    def post(self):
        form = RegistrationForm(self.request.form)
        if form.validate():
            return JsonResponse(message="form submission done.")
    
def home(request):
    return JsonResponse(dict(request.headers))