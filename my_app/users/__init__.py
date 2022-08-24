from flask import Blueprint
from flask_restful import Api
from .resources import Users

users = Blueprint('users', __name__, url_prefix='/users')

api = Api(users)

api.add_resource(Users, '/')