from navycut.core import models
from navycut.datastructures import NCObject

# create your models here: 

#demo models

class Aniket:
    def save(self):
        models.session.add(self)
        models.session.commit()

class Blog(models.Model):
    id = models.Column(models.Integer, primary_key=True, unique=True)
    name = models.Column(models.String(255), nullable=False, unique=True)
    subject = models.Column(models.String(255), nullable=False)
    body = models.Column(models.String(), nullable=False)
    is_active = models.Column(models.Boolean, default=True)

    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "subject":self.subject,
            "body":self.body,
            "is_active":self.is_active,
        }

    def to_ncobject(self):
        return NCObject(
            id=self.id,
            name=self.name,
            subject=self.subject,
            body=self.body,
            is_active=self.is_active
        )

    # def save(self, *args, **kwargs):
    #     models.session.add(self)
    #     models.session.commit()