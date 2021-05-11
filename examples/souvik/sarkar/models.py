from navycut.orm import db

# create your models here: 
#demo models

class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.String(), nullable=False)
    head_image = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

class Doraemon(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.String(), nullable=False)
    head_image = db.Column(db.String(255), nullable=True)
    body_picture = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

class MotuPatlu(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.String(), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

class Kiteretsu(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), nullable=False, unique=True, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.String(), nullable=False)
    is_active = db.Column(db.Boolean, default=True)