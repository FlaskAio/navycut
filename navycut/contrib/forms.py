"""
It's using the default wtforms for 
form creation and validation.
"""

from wtforms import *
from wtforms_sqlalchemy.orm import model_form
from flask_wtf import FlaskForm as Form
from navycut.orm.sqla import sql


class ModelForm:
    """
    for example::

        from naycuts.contrib import forms

        class BlogForm(forms.ModelForm):
            model = Blog
    """
    model=None

    def __init__(self):
        self.form = model_form(self.model, db_session=sql.session)
    
    def __call__(self, req_form=None, instance=None):
        self.former = self.form(req_form, obj=instance)
        return self.former