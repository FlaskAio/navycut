from flask_sqlalchemy import BaseQuery as _BaseQuery

class BaseQuery(_BaseQuery):
    """
    The dafault query class.
    It's a subclass of Flask_Sqlalchemy baseQuery class.
    It comes with some extra and advance query features.
    """
    def __init__(self, *wargs, **kwargs) -> None:
        super(BaseQuery, self).__init__(*wargs, **kwargs)

    # def exclude(self, **kwargs):
    #     objL:list = self.query.all()
    #     ans = []
    #     for obj in objL:
    #         pass