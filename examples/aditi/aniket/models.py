from navycut.orm import sql
# from sqlalchemy.orm.decl_api import Model

# create your models here: 
# demo models

class Blog(sql.Model):
    # id = sql.fields.Integer(pk=True, unique=True)
    name = sql.fields.Char(required=True, unique=True)
    picture = sql.fields.Image()
    body = sql.fields.Text(required=False)
    author_id = sql.fields.ForeignKey("Author")
    author = sql.fields.Relationship("Author")
    is_active = sql.fields.Boolean(default=True)

class Author(sql.Model):
    # id = sql.fields.Integer(pk=True, unique=True)
    name = sql.fields.Char(required=True, unique=True)
    picture = sql.fields.Image()
    is_active = sql.fields.Boolean(default=True)

    def __repr__(self):
        return self.name

class ExtraUser(sql.Model):
    # id = sql.fields.Integer(pk=True, unique=True)
    user = sql.fields.Relationship("User", backref="extra_user")
    user_id = sql.fields.ForeignKey("User")
    father_name = sql.fields.Char(required=True, unique=True)