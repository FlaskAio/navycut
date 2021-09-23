### Introduction

A model is the single, definitive source of information about your data. It contains the essential fields and behaviors of the data you’re storing. Generally, each model maps to a single database table. Here by default we are using Flask-SQLAlchemy ORM for model layer.

__The basics:__

- Each model is a Python class that subclasses navycut.orm.sqla.sql.Model.
- Each attribute of the model represents a database field.
- With all of this, Navycut gives you an automatically-generated database-access API.

### Quick Example
This example model defines a Person, which has a first_name and last_name:
```python
from navycut.orm import sql

class Person(models.Model):
    first_name = sql.fields.Char(max_length=30)
    last_name = sql.fields.Char(max_length=30)
```
`first_name` and `last_name` are fields of the model. Each field is specified as a class attribute, and each attribute maps to a database column.

The above **Person** model would create a database table like this:

```sql
CREATE TABLE person (
    "id" serial NOT NULL PRIMARY KEY,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL
);
```

### Using Models

Once you have defined your models, you need to tell Navycut you’re going to use those models. Do this by editing your settings file and changing the **INSTALLED_APPS** setting to add the name of the module that contains your models.py.

For example, if the models for your application live in the module __myapp.models__ (the package structure that is created for an application by the __manage.py createapp__ script), **INSTALLED_APPS** should read, in part:
```python
INSTALLED_APPS = [
    #...
    'myapp',
    #...
```
When you add new apps to **INSTALLED_APPS**, be sure to run __manage.py migrate__, optionally making migrations for them first with __manage.py makemigrations__.

### Fields
The most important part of a model – and the only required part of a model – is the list of database fields it defines. Fields are specified by class attributes. Be careful not to choose field names that conflict with the models API like __clean__, __save__, or **delete**. 
Here we are using the sqlalchemy default fields and added some more custom fields like `ImageField` or `JsonField`.

field_class : `navycut.orm.sqla.fields.Fields`

**Example**
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

### Field Types
Each field in your model should be an instance of the appropriate Field class. Navycut uses the field class types to determine a few things:

The column type, which tells the database what kind of data to store (e.g. __INTEGER, VARCHAR, TEXT__).
The default HTML widget to use when rendering a form field (e.g. **`<input type="text">, <select>`**).
The minimal validation requirements, used in Navycut’s admin and in automatically-generated forms.
Navycut ships with dozens of built-in field types. Internally it's using SQLAlchemy module to deliver the services and apis.

##### Char

__method => Fields.Char(max_length:int=255, required:bool=False, pk:bool=False, unique:bool=False, choices:tuple=None,help_text:str=None)__  
A string field, for small- to large-sized strings.

For large amounts of text, use TextField.

##### Text

__method => Fields.Text(required:bool=False, unique:bool=False, help_text:str=None, widget:str="ckeditor")__  
- wdiget:  
Declare the text widget are box for admin section.
Default is "ckeditor".
available options - "ckeditor", "tinymce"

##### Float

__method => Fields.Float(required:bool=False, unique:bool=False, pk:bool=False,choices:tuple=None,help_text:str=None)__  
The Float fields for sqlalchemy,

##### Integer
__method => Fields.Integer(required:bool=False, unique:bool=False, pk:bool=False,choices:tuple=None,help_text:str=None)__  

##### BigInteger
__method => Fields.BigInteger(required:bool=False, unique:bool=False, pk:bool=False,choices:tuple=None,help_text:str=None)__  

##### SmallInteger
__method => Fields.SmallInteger(required:bool=False, unique:bool=False, pk:bool=False,choices:tuple=None,help_text:str=None)__  

##### Boolean
__method => Fields.Boolean(required:bool=False, unique:bool=False, default:bool=False, help_text:str=None)__  

##### Json
__method => Fields.Json(required:bool=False, default={}, help_text:str=None)__  

##### Image
__method => Fields.Image(required:bool=False, help_text:str=None)__

##### Binary
__method => Fields.Binary(required:bool=False, default=None, help_text:str=None)__ 

##### LargeBinary
__method => Fields.LargeBinary(required:bool=False, default=None, help_text:str=None)__ 

##### Time
__method => Fields.Time(required:bool=False, default=None, help_text:str=None, choices:tuple=None)__ 

##### Date
__method => Fields.Date(required:bool=False, default=None, help_text:str=None, choices:tuple=None)__

##### DateTime
__method => Fields.DateTime(required:bool=False, default=None, help_text:str=None, choices:tuple=None)__

##### ForiegnKey
__method => Fields.ForiegnKey(model:str,unique:bool=False,required:bool=False,help_text:str=None)__

##### OneToOne
__method => Fields.OneToOne(model:str, backref:str, uselist:bool = False,)__

##### ManyToOne
__method => Fields.ManyToOne(model:str, backref:str, uselist:bool = False,)__
### Field Options
Each field takes a certain set of field-specific arguments (documented in the model field reference). For example, CharField (and its subclasses) require a max_length argument which specifies the size of the VARCHAR database field used to store the data.

There’s also a set of common arguments available to all field types. All are optional. They’re fully explained in the reference, but here’s a quick summary of the most often-used ones:

__max_length__  
The maximum length of the field. only applicable for Cahr field.
Default value is 255.

__required__  
If False, the field is allowed to be blank. Default is False.

__pk__  
If True, this field is the primary key for the model.

**unique**  
If True, this field must be unique throughout the table.

__help_text__  
Extra `help` text to be displayed with the form widget. 
It’s useful for documentation even if your field isn’t used on a form.

__choices__  
A sequence consisting itself of iterables of exactly two items 
(e.g. [(A, B), (A, B) ...]) to use as choices for this field. 
If choices are given, they’re enforced by model validation and 
the default form widget will be a select box with these choices 
instead of the standard text field.

A choice list should look like this:
```python
YEAR_IN_SCHOOL_CHOICES = [
    ('FR', 'Freshman'),
    ('SO', 'Sophomore'),
    ('JR', 'Junior'),
    ('SR', 'Senior'),
    ('GR', 'Graduate'),
]
```
The first element in each tuple is the value that will be stored in the database. The second element is displayed by the field’s form widget.

Given a model instance, the display value for a field with `choices` can be accessed using the `get_FOO_display()` method. For example:
```python
from navycut.orm import sql

class Person(sql.Model):
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    name = sql.fields.Char(max_length=60)
    shirt_size = sql.fields.Char(max_length=1, choices=SHIRT_SIZES)
```
```python
>>> p = Person(name="Fred Flintstone", shirt_size="L")
>>> p.save()
>>> p.shirt_size
'L'
>>> p.get_shirt_size_display()
'Large'
```

### Automatic primary key fields
By default, Navycut gives each model an auto-incrementing primary key with the type specified per app. For example:
```python
id = sql.fields.Integer(pk=True)
```
If you’d like to specify a custom primary key, specify pk=True on one of your fields.

### Relationships

Clearly, the power of relational databases lies in relating tables to each other. Navycut offers ways to define the three most common types of database relationships: many-to-one, many-to-many and one-to-one.

#### Many-to-one relationships

To define a many-to-one relationship, use `Navycut.orm.sqla.fields.Fields.ManyToOne` You use it just like any other Field type: by including it as a class attribute of your model also you need to add a `Navycut.orm.sqla.fields.Fields.ForiegnKey` filed with the connectable model class.

For example, if a Blog model has a Author – that is, a Author makes multiple blogs but each Blog only has one Author – use the following definitions:
```python
from navycut.orm.sqla import sql

class Blog(sql.Model):
    id = sql.fields.Integer(pk=True, unique=True)
    heading = sql.fields.Char(required=True, unique=True)
    author = sql.fields.ManyToOne("Author")

class Author(sql.Model):
    id = sql.fields.Integer(pk=True, unique=True)
    name = sql.fields.Char(required=True, unique=True)
    blog_id = sql.fields.ForiegnKey("Blog")
```

#### One-to-one relationship
To define the OneToOne relationship please use `Navycut.orm.sqla.fields.Fields.OneToOne` and don't forgot to use `Navycut.orm.sqla.fields.Fields.ForiegnKey` because it's required for every kind of relation.

For example, Here we have added two models one is Blog and another one is Author. Now the desired relation is one author can publish only one blog post. Check the below example to check the implementation procedure.
```python
from navycut.orm.sqla import sql

class Blog(sql.Model):
    id = sql.fields.Integer(pk=True, unique=True)
    heading = sql.fields.Char(required=True, unique=True)
    author = sql.fields.OneToOne("Author")

class Author(sql.Model):
    id = sql.fields.Integer(pk=True, unique=True)
    name = sql.fields.Char(required=True, unique=True)
    blog_id = sql.fields.ForiegnKey("Blog", unique=True)
```

#### Many-to-many relationship
Curently we don't have any special method tod define the many-to-manu relationship. You can use the default SQLAlchemy process to implement the Many-to-many relationship.

### Making Queries
Once you’ve created your data models, Navycut automatically gives you a database-abstraction API that lets you create, retrieve, update and delete objects. Since it's using SQLAlchemy module so the queries APIs are same with it.

We are contiously trying to develop some more features and APIs for the query section. Please be in touch for the latest code update.

For original documentation of SQLAlchemy quries please [click here](https://docs.sqlalchemy.org/en/14/orm/query.html)

#### Create a new object
Please check teh below example to learn more about the data creation procedure of Navycut framework:
```python
>>> from blog.models import Blog
>>> b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
>>> b.save()
```
#### Delete a Object
```python
>>> from blog.models import Blog
>>> b = Blog.query.get(1)
>>> b.delete()
```

### Migration

Migrations are Navycut’s way of propagating changes you make to your models (adding a field, deleting a model, etc.) into your database schema. They’re designed to be mostly automatic, but you’ll need to know when to make migrations, when to run them, and the common problems you might run into. Navycut is using `flask-migrate` module to deliver this service.

#### The Commands
There are several commands which you will use to interact with migrations and Navycut’s handling of database schema:

**migrate**, which is responsible for applying and unapplying migrations.
**makemigrations**, which is responsible for creating new migrations based on the changes you have made to your models.
**sqlmigrate**, which displays the SQL statements for a migration.

You should think of migrations as a version control system for your database schema. makemigrations is responsible for packaging up your model changes into individual migration files - analogous to commits - and migrate is responsible for applying those to your database.