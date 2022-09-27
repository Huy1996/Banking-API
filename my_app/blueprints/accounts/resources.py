from flask_restful import Resource, reqparse, request
from my_app.models import Account, AccountType
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from sqlalchemy import exc
from decimal import Decimal

str_require = {
    "type": str,
    "required": True,
    "help": "This field cannot be blank."
}

float_require = {
    "type": Decimal,
    "required": True,
    "help": "This field cannot be blank."
}

_account_create = reqparse.RequestParser()
_account_create.add_argument('account_type', **str_require)

_account_deposit = reqparse.RequestParser()
_account_deposit.add_argument("account_id", **str_require)
_account_deposit.add_argument("amount", **float_require)
_account_deposit.add_argument("image", **str_require)

_account_transfer = reqparse.RequestParser()
_account_transfer.add_argument("receiver", **str_require)
_account_transfer.add_argument("amount", **float_require)


class BankAccount(Resource):
    def __init__(self):
        verify_jwt_in_request()
        self.user_id = get_jwt_identity()["user_id"]

    def get(self):
        account_list = Account.find_by_user_id(self.user_id)
        if account_list:
            account_list = [account.to_json() for account in account_list]
            return account_list, 200
        else:
            return None, 200

    def post(self):
        data = _account_create.parse_args()
        account = Account(AccountType[data["account_type"]], self.user_id)
        try:
            account.save_to_db()
            return {"message": "Account create successful"}, 200
        except exc.IntegrityError:
            return {"message": "Something Happen"}, 400

    def put(self):
        pass


class Deposit(Resource):
    def __init__(self):
        verify_jwt_in_request()
        self.user_id = get_jwt_identity()["user_id"]
        self.data = _account_deposit.parse_args()

    def post(self):
        account = Account.find_by_id(self.data["account_id"])
        if account and str(account.user_id) == self.user_id:
            transaction = account.deposit(self.data["amount"], self.data["image"])
            return transaction.to_json(),200
        else:
            return {"message": "Invalid request."}, 400


class AccountAction(Resource):
    def __init__(self):
        verify_jwt_in_request()
        self.user_id = get_jwt_identity()["user_id"]


class Transaction(AccountAction):
    def get(self, account_id):
        account = Account.find_by_id(account_id)
        if account and str(account.user_id) == self.user_id:
            transaction_list = account.transactions
            if transaction_list:
                transaction_list = [transaction.to_json() for transaction in transaction_list]
                return transaction_list, 200
        else:
            return {"message": "Invalid request."}, 400


class Transfer(AccountAction):
    def post(self, account_id):
        account = Account.find_by_id(account_id)
        data = _account_transfer.parse_args()
        if account and str(account.user_id) == self.user_id:
            transaction = account.transfer(data["receiver"], data["amount"])
            return transaction.to_json(), 200
        else:
            return {"message": "Invalid request."}, 400