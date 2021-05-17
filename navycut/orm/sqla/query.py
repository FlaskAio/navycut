from flask_sqlalchemy import BaseQuery as _BaseQuery

class BaseQuery(_BaseQuery):
    pass
    # def exclude(self, **kwargs):
    #     objL:list = self.query.all()
    #     ans = []
    #     for obj in objL:
    #         pass