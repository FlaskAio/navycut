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



# class Bike(sql.Model):
#     id = sql.Column(sql.Integer, primary_key=True, unique=True)
#     name = sql.field.Char(max_length=255, choices=(('duke', 'DUKE'), ('rc', 'RC')), help_text="this is name field.")
#     model = sql.field.Char(required=True, choices=(('200', '200'), ('390', '390')), help_text="this is subject field.")
#     image = sql.field.Image(required=True)
#     is_active = sql.Column(sql.Boolean, default=True)
#     # aniket_id = sql.field.ForeignKey("aniket.id")
#     aniket_id = sql.Column(sql.Integer, sql.ForeignKey("aniket.id"))

#     def __repr__(self):
#         return self.name

# class Aniket(sql.Model):
#     id = sql.Column(sql.Integer, primary_key=True, unique=True)
#     name = sql.field.Char(max_length=255, choices=[('aniket', 'Aniket'), ('gobind', 'Gobind')], help_text="this is name field.")
#     subject = sql.field.Char(required=True, choices=(('Plassey', 'PLASSEY'), ('Chakdah', 'CHAKDAH')), help_text="this is subject field.")
#     body = sql.field.Json()
#     profile_image = sql.field.Image(required=True)
#     data = sql.field.Image(required=True)
#     duration = sql.Column(sql.SmallInteger)
#     is_active = sql.Column(sql.Boolean, default=True)
#     # bike = sql.field.OneToMany("Bike", backref="anike")
#     bike = sql.relationship("Bike", backref="anike")


class Cycle(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True, unique=True)
    name = sql.field.Char(max_length=255, choices=(('duke', 'DUKE'), ('rc', 'RC')), help_text="this is name field.")
    model = sql.field.Char(required=True, choices=(('200', '200'), ('390', '390')), help_text="this is subject field.")
    image = sql.field.Image(required=True)
    is_active = sql.Column(sql.Boolean, default=True)
    kunal_id = sql.field.ForeignKey("Owner")
    # kunal_id = sql.Column(sql.Integer, sql.ForeignKey("kunal.id"))

    def __repr__(self):
        return self.name

class Owner(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True, unique=True)
    name = sql.field.Char(max_length=255, choices=[('aniket', 'Aniket'), ('gobind', 'Gobind')], help_text="this is name field.")
    subject = sql.field.Char(required=True, choices=(('Plassey', 'PLASSEY'), ('Chakdah', 'CHAKDAH')), help_text="this is subject field.")
    body = sql.field.Json()
    is_active = sql.Column(sql.Boolean, default=True)
    bike = sql.field.OneToMany("Cycle", backref="kunal")
    # cycle = sql.relationship("Cycle", backref="aniket")
    def __repr__(self):
        return self.name