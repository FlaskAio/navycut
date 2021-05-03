from flask_sqlalchemy import BaseQuery, SQLAlchemy as _SQLAlchemy
from flask_sqlalchemy.model import Model
from flask_sqlalchemy import BaseQuery
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from navycut.errors.models import ModelsIntegrityError
from navycut.datastructures import NCObject

# class _object(object):
#     def __init__(self, model,*args, **kwargs):
#         self.models = model
#     def all(self):
#         return self.models.query.all()

# class _BaseQuery(BaseQuery):
#     def exclude(self, **kwargs):
#         objL:list = self.query.all()
#         ans = []
#         for obj in objL:
#             pass

class _Model(Model):
    def __init__(self, *args, **kwargs):
        # self.object = _object(self)
        super(_Model, self).__init__(*args, **kwargs)
    def save(self):
        db.session.add(self)
        try: db.session.commit()
        except IntegrityError as e: raise ModelsIntegrityError(e)
    def all(self):
        return self.query.all()

    def to_dict(self) -> dict:
        """returns the dictionary output of the particular model."""
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        
    def to_ncobject(self) -> NCObject:
        """returns the NCObject output of the particular model."""
        return NCObject(self.to_dict())

class NavycutORM(_SQLAlchemy):
    """
    The default database for Navycut Fullstack framework. Basically
    it's a subclass of SQLALchemy. It contains all the sqlalchemy features
    with some extra own's special.
    """
    def __init__(self):
        super(NavycutORM, self).__init__(model_class=_Model)

db = NavycutORM()
