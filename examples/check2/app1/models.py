from navycut.orm import sql

# create your models here: 
#demo models

class Blog(sql.Model):
    id = sql.field.Integer(pk=True, unique=True)
    name = sql.field.Char(required=True, unique=True)
    picture = sql.field.Image(required=True)
    body = sql.field.Text(required=False)
    is_active = sql.field.Boolean(default=True)

class Polls(sql.Model):
    id = sql.field.Integer(pk=True, unique=True)
    name = sql.field.Char(required=True, unique=True)
    picture = sql.field.Image(required=True)
    body = sql.field.Text(required=False)
    is_active = sql.field.Boolean(default=True)