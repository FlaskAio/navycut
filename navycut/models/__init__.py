from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy

class NavycutORM(_SQLAlchemy):
    def __init__(self):
        super(NavycutORM, self).__init__()

    def save(self):
        pass
        # self.session.add()

models = NavycutORM()
