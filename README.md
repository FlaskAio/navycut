# Navycut

<img src="https://raw.githubusercontent.com/flaskAio/navycut/main/logos/navycut_logo.png">
<br>

# Downloads
[![Downloads](https://pepy.tech/badge/navycut)](https://pepy.tech/project/navycut) [![Downloads](https://pepy.tech/badge/navycut/month)](https://pepy.tech/project/navycut/month) [![Downloads](https://pepy.tech/badge/navycut/week)](https://pepy.tech/project/navycut/week)
<br>

#### contributor wanted : feel free to contact me at aniketsarkar@yahoo.com

Navycut is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. Thanks for checking it out.

It's actually a Full Stack web framework using <a href="https://flask.palletsprojects.com">Flask(werkzeug)</a> as backend wsgi server and try to deliver the service and api like Django.

The official documentation is online at <a href="navycut.github.io">navycut.github.io</a>.

### Basic installation
    Use the package manager [pip](https://pypi.org/project/navycut/) to install navycut.

```bash
python3 -m pip install navycut
```
    Install from source code

```bash
git clone https://github.com/flaskAio/navycut.git && cd navycut/
python3 setup.py install
```

### check for installation
```bash
navycut --version
0.0.5
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
or 
python manage.py runserver 0.0.0.0:8000 # to start a server on different port
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
now you need to register the newly created app with the project.
To do this you must perform the following steps.
<br>

* open the directory containing the same name with project.
* open settings.py file.
* Now findout the block called `INSTALLED_APPS`.
* Under this `INSTALLED_APPS` list add your app.
* Suppose your app name is `blogapp` then add the following line under `INSTALLED_APPS`:
"blogapp.sister.BlogappSister".
<br>

Your settings.py file should look like this:

```python
INSTALLED_APPS = [
    "navycut.orm.sqla",
    "navycut.contrib.cors",
    "navycut.contrib.auth",
    "navycut.contrib.mail",
    "navycut.contrib.admin",
    "navycut.helpers.upload_server",
    "blogapp"
]
```

### All available command you must know to work with Navycut
* to know more about the available commands:
```bash
navycut --help
```
* to create a project directory at the present location:
```bash
navycut createproject project_name
```
* to create a app inside the project directory:
```bash
cd project_name
python manage.py createapp app_name
```
* to migrate the database:
```bash
python manage.py migrate
```
* to apply the migration to the database:
```bash
python manage.py makemigrations
```
* to create the superuser to access the admin:
```bash
python manage.py createsuperuser
```
* to start the interactive development server
```bash
python manage.py runserver
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
The default url_prefix is the app name i.e "/blog" for this case.
If you want to change it and use your own customized name then
plese update the url_prefix for a particular app on the sister.py file
under the AppSister class.
"""

urlpatterns = [
    path('/', views.BlogView, name='blog-index'),
    url('/<int:id>', views.blog_detail, name='blog-detail'),
    url('/search/?id=1', views.blog_search, name='blog-search'),
	include('/polls', 'polls.urls') # include urlpatterns from another app
]
```
```python
# views.py

from navycut.urls import MethodView
from .models import Blog

"""
Here you can use views method like expressJs.
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
@group_required('super_admin')
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
<br/>

##### If you are from India, You can donate directly Using VPA(UPI):

    my vpa id: aniketsarkar@ybl
<a href="https://cdn.worldvectorlogo.com/logos/phonepe-1.svg">
<img src="https://download.logo.wine/logo/PhonePe/PhonePe-Logo.wine.png" height="120px" width="180px">
</a>
<br>
<a href="https://paytm.me/vA-DF7O">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Paytm_Logo_%28standalone%29.svg/1200px-Paytm_Logo_%28standalone%29.svg.png" height="50px" width="100px">
</a>

### Contributors

<a href="https://github.com/flaskAio/navycut/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=flaskAio/navycut" />
</a>

### How to contribute

* Fork and clone this repository
* Make some changes as required
* Write unit test to showcase its functionality
* Submit a pull request under `main` branch

### How to run this project on your local machine

* Fork and clone this repository
* Create a virtual environment using python virtualenv module on the project root directory.
* Activate the virtual environment and install the package dependencies mentioned on `requirements.txt` file.
* Now run this command : `python setup.py install`. This command will install `navycut` on the virtual environment. 
* Make any changes on your local code.
* Run again the command : `python setup.py install`.
* Now create a separate project inside the example folder and start testing for your code changes.
* If you face any difficulties to perform the above steps, then plese contact me at: `aniketsarkar@yahoo.com`.

# License

GNU General Public License v3 or later (GPLv3+)

Copyright (c) 2021 navycut(aniketsarkar@yahoo.com)