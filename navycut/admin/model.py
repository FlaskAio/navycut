from ..models import models
from datetime import datetime
from flask_login import UserMixin

class BaseUser(models.Model, UserMixin):
    id = models.Column(models.Integer, primary_key=True)
    username = models.Column(models.String(20), unique=True, nullable=False)
    name = models.Column(models.String(255), nullable=False)
    email = models.Column(models.String(100), nullable=False, unique=True)
    password = models.Column(models.String(100), nullable=False)
    is_active = models.Column(models.Boolean, default=True)
    created_at = models.Column(models.DateTime, default=datetime.now)