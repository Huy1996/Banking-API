from flask import Blueprint
from flask_restful import Api

accounts = Blueprint('accounts', __name__, url_prefix='/accounts')

api = Api(accounts)
