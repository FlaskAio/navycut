from navycut.contrib import forms 

class AdminLoginForm(forms.Form):
    username = forms.StringField("Your Username", 
                    [forms.validators.Required("Please enter your username.")])
                    
    password = forms.PasswordField("Your Password",
                    [forms.validators.Required("Please enter your password.")])