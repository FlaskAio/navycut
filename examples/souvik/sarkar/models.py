from navycut.orm.sqla import sql
# from navycut.orm.sql import meta

# create your models here: 
#demo models

# class Blogs(sql.Model):
#     id = sql.Column(sql.Integer, primary_key=True, unique=True)
#     name = sql.Column(sql.String(255), nullable=False, unique=True)
#     subject = sql.Column(sql.String(255), nullable=False)
#     body = sql.Column(sql.String(), nullable=False)
#     head_image = sql.Column(sql.String(255), nullable=True)
#     is_active = sql.Column(sql.Boolean, default=True)

# class Doraemon(sql.Model):
#     id = sql.Column(sql.Integer, primary_key=True, unique=True)
#     name = sql.Column(sql.String(255), nullable=False, unique=True)
#     subject = sql.Column(sql.String(255), nullable=False)
#     body = sql.Column(sql.String(), nullable=False)
#     head_image = sql.Column(sql.String(255), nullable=True)
#     body_picture = sql.Column(sql.String(255), nullable=True)
#     is_active = sql.Column(sql.Boolean, default=True)

# class MotuPatlu(sql.Model):
#     id = sql.Column(sql.Integer, primary_key=True, unique=True)
#     name = sql.Column(sql.String(255), nullable=False, unique=True)
#     subject = sql.Column(sql.String(255), nullable=False)
#     body = sql.Column(sql.String(), nullable=False)
#     is_active = sql.Column(sql.Boolean, default=True)

# class Kiteretsu(sql.Model):
#     id = sql.Column(sql.Integer, primary_key=True, unique=True)
#     name = sql.Column(sql.String(255), nullable=False, unique=True, primary_key=True)
#     subject = sql.Column(sql.String(255), nullable=False)
#     body = sql.Column(sql.String(), nullable=False)
#     is_active = sql.Column(sql.Boolean, default=True)

# # class Nobita(sql.Model):
# #     id = sql.Column(sql.Integer, primary_key=True, unique=True)
# #     # print (dir(sql.Model))
# #     # tame = sql.Column(sql.String(255))
# #     tame = sql.CharField(max_length=255)
# #     subject = sql.Column(sql.String(255), nullable=False)
# #     body = sql.Column(sql.String(), nullable=False)
# #     is_active = sql.Column(sql.Boolean, default=True)

# class Suzuka(sql.Model):
#     id = sql.Column(sql.Integer, primary_key=True, unique=True)
#     # print (dir(sql.Model))
#     # tame = sql.Column(sql.String(255))
#     tame = sql.field.Char(max_length=255)
#     subject = sql.Column(sql.String(255), nullable=False)
#     body = sql.Column(sql.String(), nullable=False)
#     is_active = sql.Column(sql.Boolean, default=True)

# class Partha(sql.Model):
#     id = sql.Column(sql.Integer, primary_key=True, unique=True)
#     name = sql.field.Char(max_length=255)
#     subject = sql.Column(sql.String(255), nullable=False)
#     body = sql.Column(sql.String(), nullable=False)
#     profile_image = sql.field.Image(required=True)
#     data = sql.field.Image(required=True)
#     duration = sql.Column(sql.Interval())
#     is_active = sql.Column(sql.Boolean, default=True)

class Aniket(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True, unique=True)
    name = sql.field.Char(max_length=255, choices=[('aniket', 'Aniket'), ('gobind', 'Gobind')], help_text="this is name field.")
    subject = sql.field.Char(required=True, choices=(('plassey', 'PLASSEY'), ('Chakdah', 'CHAKDAH')), help_text="this is subject field.")
    body = sql.field.Json()
    profile_image = sql.field.Image(required=True)
    data = sql.field.Image(required=True)
    duration = sql.Column(sql.SmallInteger)
    is_active = sql.Column(sql.Boolean, default=True)