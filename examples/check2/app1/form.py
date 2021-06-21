from navycut.contrib import forms

class RegistrationForm(forms.Form):
    username = forms.StringField('Username', [forms.validators.Length(min=4, max=25)])
    email = forms.StringField('Email Address', [forms.validators.Length(min=6, max=35)])
    password = forms.PasswordField('New Password', [
        forms.validators.DataRequired(),
        forms.validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = forms.PasswordField('Repeat Password')
    accept_tos = forms.BooleanField('I accept the TOS', [forms.validators.DataRequired()])