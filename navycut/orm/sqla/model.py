from flask_sqlalchemy.model import Model as _Model
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.inspection import inspect
from navycut.errors.models import ModelsIntegrityError
from navycut.errors.misc import NCBaseError
from navycut.datastructures import NCObject
from flask import current_app
from .fields import Fields

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
        try: 
            current_app.extensions['sqlalchemy'].db.session.commit()

        except IntegrityError as e: 
            raise ModelsIntegrityError(e)

        except Exception as e:
            raise NCBaseError(e)

    def delete(self):
        """
        To delete a record object.
        """
        current_app.extensions['sqlalchemy'].db.session.delete(self)
        current_app.extensions['sqlalchemy'].db.session.commit()

    def to_dict(self) -> dict:
        """
        returns the dictionary output of the particular model.
        """
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        
    def to_ncobject(self) -> NCObject:
        """
        returns the NCObject output of the particular model.
        """
        return NCObject(self.to_dict())

    def __repr__(self) -> str:
        return super(Model, self).__repr__()

    @declared_attr
    def id(self):
        return Fields.Integer(pk=True, 
                            unique=True, 
                            required=True, 
                            help_text="default id field for every model.")