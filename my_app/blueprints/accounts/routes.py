from flask import Blueprint
from flask_restful import Api
from .resources import BankAccount

accounts = Blueprint('accounts', __name__, url_prefix='/accounts')

api = Api(accounts)
api.add_resource(BankAccount, '/')