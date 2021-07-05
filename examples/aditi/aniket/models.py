from navycut.orm import sql

# create your models here: 
# demo models

class Blog(sql.Model):
    id = sql.fields.Integer(pk=True, unique=True)
    name = sql.fields.Char(required=True, unique=True)
    picture = sql.fields.Image(required=True)
    body = sql.fields.Text(required=False)
    author_id = sql.fields.ForeignKey("Author")
    author = sql.fields.ManyToOne("Author", backref="blogs")
    is_active = sql.fields.Boolean(default=True)

class Author(sql.Model):
    id = sql.fields.Integer(pk=True, unique=True)
    name = sql.fields.Char(required=True, unique=True)
    picture = sql.fields.Image(required=True)
    is_active = sql.fields.Boolean(default=True)

class ExtraUser(sql.Model):
    id = sql.fields.Integer(pk=True, unique=True)
    user = sql.fields.OneToOne("User", backref="extra_user")
    user_id = sql.fields.ForeignKey("User")
    father_name = sql.fields.Char(required=True, unique=True)