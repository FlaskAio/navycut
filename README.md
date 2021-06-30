# Navycut

<img src="https://i.ibb.co/q9MKYZP/navycut-logo.png">
<br>

#### contributor wanted : feel free to contact me at aniketsarkar@yahoo.com

Navycut is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. Thanks for checking it out.

It's actually a Fullstack web framework using flask as backend wsgi server and trying to deliver the service like Django does.

The official documentation is hosted on <a href="navycut.github.io">navycut.github.io</a>.

### Basic installation
    Use the package manager [pip](https://pypi.org/project/navycut/) to install foobar.

```bash
python3 -m pip install navycut
```
    Install from source code

```bash
git clone https://github.com/navycut/navycut.git && cd navycut/
python3 setup.py install
```

### check for installation
```bash
navycut version
1.0.0
```

### Introduction to Navycut
Navycut promises to deliver the fullstack service using the following features:

<ul>
    <li>Customished ORM using SQLAlchemy.</li>
        <ul>
            <li>It's comes with all the sqlalchemy features with some extra features.</li>
            <li>It's have the own Image, Json, Text, Integer, String and many others fileds like Django ORM has.</li>
            <li>Some fileds have the default choices system to add value by providing a tuple data like Django ORM.</li>
        </ul>
    <li>Inbuild Admin system using flask-admin. So all the flask-admin features are applicable here.</li>
    <li>Inbuild authentication stystem using flask-login.</li>
    <li>Form system using wt-forms.</li>
    <li>SMTP mail integration using flask-mail.</li>
    <li>Flask-migrate to migrate the database.</li>
    <li>Custom app features like django.</li>
    <li>ExpressJs like view functions to provide more interactive service.</li>
</ul>

### if you need any help to understand the command line, please try following
```bash
navycut --help
or
navycut [COMMAND] --help
```

### create the first project
```bash
navycut createproject blog
```
This command will create a project directory containing the basic files created by navycut at the specified location.

The directory structure will be:

```text
blog
├── blog
│   ├── asgi.py
│   ├── settings.py
│   ├── test.py
│   └── wsgi.py
├── templates
│   └── README.md
├── manage.py
```

### start the development server

```bash
python manage.py runserver
or python manage.py runserver 0.0.0.0:8000 # to start a server on different port
```
This command will start the development server on localhost:8888 or the provided address.
Now you should create an app to start writing the urls and appropriate views function.

### create the first app

```bash
python manage.py createapp blogapp
```
This command will create an app directory containg some navycut specified file at the project directory location.

The app folder structure will be:
```bash
blogapp
├── admin.py
├── __init__.py
├── models.py
├── sister.py
├── urls.py
└── views.py
```
Now the Project folder structure will be:
```bash
blog
├── blog
│   ├── asgi.py
│   ├── settings.py
│   ├── test.py
│   └── wsgi.py
├── blogapp
│   ├── admin.py
│   ├── __init__.py
│   ├── models.py
│   ├── sister.py
│   ├── urls.py
│   └── views.py
├── templates
|   └── README.md
├── manage.py
```
### Introduction to the model layer

```python
from navycut.orm import sql
from datetime import datetime

class Blog(sql.Model):
    id = sql.fields.Integer(pk=True)
    title = sql.fields.Char(max_length=50)
    body = sql.fields.Text(required=True)
    image = sql.fields.Image(required=True)
    created_at = sql.fields.DateTime(default=datetime.now)
    author_ptr_id = sql.fields.ForeignKey("Author")

class Author(sql.Model):
    id = sql.fields.Integer(pk=True)
    name = sql.fields.Char(max_length=100, required=True)
    image = sql.fields.Image(required=True)
    blog = sql.fields.OneToMany("Blog")

```
### Introduction to the Urls and Views Layer

```python
# urls.py
from navycut.urls import path, url, include
from . import views

"""
The default url_prefix is the app name i.e "/band" for this case.
If you want to change it and use your own customized name then
plese update the url_prefix for a particular app on the sister.py file
under the AppSister class.
"""

urlpatterns = [
    path('/', views.BlogView, name='band-list'),
    url('/<int:id>', views.blog_detail, name='band-detail'),
    url('/search/?id=1', views.blog_search, name='band-search'),
	include('/polls', 'polls.urls') # include urlpatterns from another app
]
```
```python
# views.py

from navycut.urls import MethodView
from .models import Band

"""
Here you can use views mnethod like expressJs.
Just simply pass the request and response object as
arguments of the view function.
"""
class BlogView(MethodView):
    def get(self):
        blogs = Blog.query.all()
        return self.render('blog/blog_listing.html', {'blogs': blogs})

def blog_details(req, res, id):
    blog = Blog.query.get(id)
	return res.json(blog)

def blog_search(req, res):
    id = int(req.args.get('id'))
    blog = Blog.query.get(id)
	return res.json(blog)
```

### The templating view using Jinja2 Templating Engine

```html
<html>
  <head>
    <title>Blog Listing</title>
  </head>
  <body>
    <h1>All Blogs</h1>
    <ul>
    {% for blog in blogs %}
      <li>
        <h2>{{ blog.name }}</h2>
        <img src="{{blog.image}}">
      </li>
    {% endfor %}
    </ul>
</body>
```

### Fully functional form using WTForms

```python
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
```

## Inbuild Authentication system using Flask-Login

```python
from navycut.auth import login_required, current_user, group_required
from navycut.http import JsonResponse
from navycut.urls import MethodView

class AuthView(MethodView):
    @login_required
    def get(self):
        return JsonResponse(logged_in_username=current_user.username)

@login_required
@group_required('super_admin)
def get_data(req, res):
    return res.json(username=req.user.username) # current_user == req.user
```

# Customized Inbuild Admin Panel using Flask-Admin

```python
from navycut.admin import admin
from navycut.admin.site.views import NCAdminModelView
from .models import Blog, Author

class AuthorAdminModelView(NCAdminModelView):
    """Customize the look of the auto-generated admin for the Member model"""
    excluded_fields = ['name',]

admin.register_model(Blog) # Use the default options
admin.register_model(Author, AuthorAdminModelView)  # Use the customized options
```

# Development

### Sponsors

<a href="https://liberapay.com/aniketsarkar" target="_blank">
<img src="https://www.worldfuturecouncil.org/wp-content/uploads/2018/09/Donate-Button-HEART.png" height="50px" width="100px"/>
</a>

### Contributors

<a href="https://github.com/navycut/navycut/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=navycut/navycut" />
</a>

Made with [contributors-img](https://contrib.rocks).

### How to contribute

* Fork and clone this repository
* Make some changes as required
* Write unit test to showcase its functionality
* Submit a pull request under `develop` branch

# License

MIT License

Copyright (c) 2021 navycut(aniketsarkar@yahoo.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
