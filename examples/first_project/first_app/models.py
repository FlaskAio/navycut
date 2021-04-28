from navykut.core import models
from datetime import datetime

class Blog(models.Model):
    id = models.Column(models.IntegerField, primary_key=True, unique=True)
    name = models.Column(models.String(255), required=True, unique=True)
    subject = models.Column(models.String(255), required=True)
    body = models.Column(models.String(), required=True)
    is_active = models.Column(models.BooleanField(default=True))
    created_at = models.Column(models.DateTimeField, default=datetime.now)