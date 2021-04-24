# from flask_restful import  Resource
from flask.views import MethodView
# from flask_restful import Api as _Api

def path(url, views, name=None):
    name = name or views.__name__
    return (url, views, name)