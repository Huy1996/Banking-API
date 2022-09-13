from flask_restful import Resource, reqparse
from my_app.models import Account, AccountType
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from sqlalchemy import exc

str_require = {
    "type": str,
    "required": True,
    "help": "This field cannot be blank."
}

int_require = {
    "type": int,
    "required": True,
    "help": "This field cannot be blank."
}

_account_create = reqparse.RequestParser()
_account_create.add_argument('account_type', **str_require)


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
