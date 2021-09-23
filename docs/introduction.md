# Intro to Navycut

The basic introduction about the stack and features of Navyvut project.

## Object relational mapper
Deﬁne your data models entirely in Python using SQLAlchemy. You get a rich, dynamic database-access API for free — but you can still write SQL if needed.
```python
from navycut.orm import sql

class Band(sql.Model):
    """A model of a rock band."""
    id = sql.fields.Integer(pk=True)
    name = sql.fields.Char(max_length=200)
    can_rock = sql.fields.Boolean(default=True)


class Member(sql.Model):
    """A model of a rock band member."""
    id = sql.fields.Integer(pk=True)
    name = sql.fields.Char(help_text="Member's name", max_length=200)
    instrument = sql.fields.Char(choices=(
            ('g', "Guitar"),
            ('b', "Bass"),
            ('d', "Drums"),
        ),max_length = 1)
    band = sql.fields.ForeignKey("Band")
```
## Urls and Views
A clean, elegant URL scheme is an important detail in a high-quality Web application. Navycut encourages beautiful URL design and doesn’t put any cruft in URLs, like .php or .asp. To design URLs for an application, you create a Python module called a URLconf. Like a table of contents for your app, it contains a simple mapping between URL patterns and your views.
```python
from navycut.urls import path, url, include
from . import views

"""
The default url_prefix is the app name i.e "/band" for this case.
If you want to change it and use your own customized name then
plese update the url_prefix for a particular app on the sister.py file
under the AppSister class.
"""

urlpatterns = [
    path('/', views.BandView, name='band-list'),
    url('/<int:id>', views.band_detail, name='band-detail'),
    url('/search/?id=1', views.band_search, name='band-search'),
	include('/polls', 'polls.urls') # include urlpatterns from another app
]
```
```python
from navycut.urls import MethodView
from .models import Band

class BandView(MethodView):
    def get(self):
        bands = Band.query.all()
        return self.render('bands/band_listing.html', {'bands': bands})

def band_details(req, res, id):
    band = Band.query.get(id)
	return res.json(band)

def band_search(req, res):
    id = int(req.args.get('id'))
    band = Band.query.get(id)
	return res.json(band)
```
## Templates
Navycut's template language(Jinja2) is designed to strike a balance between power and ease. It’s designed to feel comfortable and easy-to-learn to those used to working with HTML, like designers and front-end developers. But it is also flexible and highly extensible, allowing developers to augment the template language as needed.
```html
<html>
  <head>
    <title>Band Listing</title>
  </head>
  <body>
    <h1>All Bands</h1>
    <ul>
    {% for band in bands %}
      <li>
        <h2>{{ band.name }}</h2>
        {% if band.can_rock %}
        <p>This band can rock!</p>
        {% endif %}
      </li>
    {% endfor %}
    </ul>
</body>
```
## Forms
Navycut provides a powerful form library using wt-form that handles rendering forms as HTML, validating user-submitted data, and converting that data to native Python types. Navycut also provides a way to generate forms from your existing models and use those forms to create and update data.
```python
class RegistrationForm(forms.Form):
    username = forms.StringField('Username', [forms.validators.Length(min=4, max=25)])
    email = forms.StringField('Email Address', [forms.validators.Length(min=6, max=35)])
    password = forms.PasswordField('New Password', [
        forms.validators.DataRequired(),
        forms.validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = forms.PasswordField('Repeat Password')
    accept_tos = forms.BooleanField('I accept the TOS', [forms.validators.DataRequired()])
```

## Authentication
Navycut comes with a full-featured and secure authentication system. It handles user accounts, groups, permissions and cookie-based user sessions. This lets you easily build sites that allow users to create accounts and safely log in/out.
```python
from navycut.auth import login_required, current_user
from navycut.http import JsonResponse
from navycut.urls import MethodView

class AuthView(MethodView):
    @login_required
    def get(self):
        return JsonResponse(logged_in_username=current_user.username)
```
## Admin Panel
One of the most powerful parts of Navycut is its automatic admin interface. It reads metadata in your models to provide a powerful and production-ready interface that content producers can immediately use to start managing content on your site. It’s easy to set up and provides many hooks for customization. Basically Navycut uses the default flask_admin module to provide this service.
```python
from navycut.admin import admin
from navycut.admin.site.views import NCAdminModelView
from .models import Band, Member

class MemberAdminModelView(NCAdminModelView):
    """Customize the look of the auto-generated admin for the Member model"""
    excluded_fields = ['name',]

admin.register_model(Band) # Use the default options
admin.register_model(Member, MemberAdminModelView)  # Use the customized options
```

## Internationalization
No service till now, need to develop.

### Security
Navycut provides multiple protections against:

- Clickjacking
- Cross-site scripting
- Cross Site Request Forgery (CSRF)
- SQL injection
- Remote code execution