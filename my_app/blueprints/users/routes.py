from flask import Blueprint
from flask_restful import Api
from .resources import Login

users = Blueprint('users', __name__, url_prefix='/users')

api = Api(users)

api.add_resource(Login, '/login')
