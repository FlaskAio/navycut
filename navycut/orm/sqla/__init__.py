from flask_sqlalchemy import SQLAlchemy
# from .model import Model
from .query import BaseQuery
from .fields import Fields
from sqlalchemy import MetaData

from flask_sqlalchemy.model import Model as _Model
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from navycut.errors.models import ModelsIntegrityError
from navycut.datastructures import NCObject


__all__ = ("sql", "meta", "Model")

class Model(_Model):

    def __init__(self, *args, **kwargs):
        super(_Model, self).__init__(*args, **kwargs)
    def save(self):
        sql.session.add(self)
        try: sql.session.commit()
        except IntegrityError as e: raise ModelsIntegrityError(e)

    def to_dict(self) -> dict:
        """returns the dictionary output of the particular model."""
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        
    def to_ncobject(self) -> NCObject:
        """returns the NCObject output of the particular model."""
        return NCObject(self.to_dict())




meta = MetaData()


class SQLANCORM(SQLAlchemy):
    """
    The default database for Navycut Fullstack framework. Basically
    it's a subclass of SQLALchemy. It contains all the sqlalchemy features
    with some extra own's special.
    """
    field = Fields()

    def __init__(self):

        super(SQLANCORM, self).__init__(model_class=Model,
                                    query_class=BaseQuery,
                                    metadata=meta)

sql = SQLANCORM()