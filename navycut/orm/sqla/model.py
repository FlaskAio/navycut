from flask_sqlalchemy.model import Model as _Model
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from navycut.errors.models import ModelsIntegrityError
from navycut.datastructures import NCObject
from flask import current_app

class Model(_Model):
    """
    The model class for sqlalchemy.
    """
    def __init__(self, *args, **kwargs):
        super(_Model, self).__init__(*args, **kwargs)

    def save(self):
        """
        To store the sqlalchemy object.
        """
        current_app.extensions['sqlalchemy'].db.session.add(self)
        try: current_app.extensions['sqlalchemy'].db.session.commit()
        except IntegrityError as e: raise ModelsIntegrityError(e)

    def to_dict(self) -> dict:
        """returns the dictionary output of the particular model."""
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        
    def to_ncobject(self) -> NCObject:
        """returns the NCObject output of the particular model."""
        return NCObject(self.to_dict())