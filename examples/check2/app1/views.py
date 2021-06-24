from navycut.urls import MethodView
from navycut.http import JsonResponse
from navycut.contrib.mail import send_html_mail
from navycut.datastructures import NCObject
from .form import RegistrationForm
from navycut.http.response import Response
import json as j

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
    
def home(res):
    return res.json(dict(message="salve mundi!"))
    # return ""
    # return Response.status(404)
    # return Response.send("aniket")
    # return Response.send()
    # return Response.send([1,2])
    # return JsonResponse(dict(request.headers))

def send_email(req):
    if req.method == "POST":
        data = NCObject(req.get_json())
        send_html_mail(data.subject, 
                data.message, 
                data.recipients,
                data.sender)
        return JsonResponse(message="email sent successfull")
    return JsonResponse(message="failed to sent email")