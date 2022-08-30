from flask import Blueprint
from flask_restful import Api
from .resources import Login, Register, User

users = Blueprint('users', __name__, url_prefix='/users')

api = Api(users)

api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(User, '/')
