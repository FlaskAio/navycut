from flask_sqlalchemy import SQLAlchemy
from .model import Model
from .query import BaseQuery
from .fields import Fields
from sqlalchemy import MetaData


__all__ = ("sql", "meta")


meta = MetaData()


class SqlaNcOrm(SQLAlchemy):
    """
    The default database for Navycut Fullstack framework. Basically
    it's a subclass of SQLALchemy. It contains all the sqlalchemy features
    with some extra own's special.
    """
    field = Fields()

    def __init__(self):

        super(SqlaNcOrm, self).__init__(model_class=Model,
                                    query_class=BaseQuery,
                                    metadata=meta)

sql = SqlaNcOrm()