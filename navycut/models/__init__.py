from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from flask_sqlalchemy.model import Model
from sqlalchemy.exc import IntegrityError
from ..errors.models import ModelsIntegrityError

class _object(object):
    def __init__(self, model,*args, **kwargs):
        self.models = model
    def all(self):
        return self.models.query.all()

class _Model(Model):
    def __init__(self, *args, **kwargs):
        self.object = _object(self)
        super(_Model, self).__init__(*args, **kwargs)
    def save(self):
        db.session.add(self)
        try: db.session.commit()
        except IntegrityError as e: raise ModelsIntegrityError(e)
    def all(self):
        return self.query.all()

class NavycutORM(_SQLAlchemy):
    def __init__(self):
        super(NavycutORM, self).__init__(model_class=_Model)

models = db = NavycutORM()
