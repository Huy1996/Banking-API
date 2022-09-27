from flask import Blueprint
from flask_restful import Api
from .resources import BankAccount, Deposit, Transaction, Transfer

accounts = Blueprint('accounts', __name__, url_prefix='/accounts')

api = Api(accounts)
api.add_resource(BankAccount, '/')
api.add_resource(Deposit, '/deposit')
api.add_resource(Transaction, '/<uuid:account_id>/transaction')
api.add_resource(Transfer, '/<uuid:account_id>/transfer')