from navycut.contrib import forms 

class AdminLoginForm(forms.Form):
    username = forms.StringField("Your Username", 
                    [forms.validators.DataRequired("Please enter your username.")])
                    
    password = forms.PasswordField("Your Password",
                    [forms.validators.DataRequired("Please enter your password.")])