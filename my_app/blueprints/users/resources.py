from flask_restful import Resource, reqparse
from my_app.extensions import bcrypt
from my_app.models import UserLogin, UserInfo
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, verify_jwt_in_request

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
_user_login = reqparse.RequestParser()
_user_login.add_argument('username', **str_require)
_user_login.add_argument('password', **str_require)

_user_login_edit = _user_login.copy()
_user_login_edit.add_argument('new_password', **str_require)

_user_info = reqparse.RequestParser()
_user_info.add_argument('first_name', **str_require)
_user_info.add_argument('last_name', **str_require)
_user_info.add_argument('email', **str_require)
_user_info.add_argument('address', **str_require)
_user_info.add_argument('city', **str_require)
_user_info.add_argument('state', **str_require)
_user_info.add_argument('zip_code', **int_require)
_user_info.add_argument('phone_number', **str_require)
_user_info.add_argument('pin', **str_require)

_user_info_edit = _user_info.copy()
_user_info_edit.remove_argument('first_name')
_user_info_edit.remove_argument('last_name')

_user_info_edit


class Login(Resource):
    def post(self):
        login_data = _user_login.parse_args()

        user = UserLogin.find_by_username(login_data["username"])
        if user and bcrypt.check_password_hash(user.password, login_data["password"]):

            user_data = UserInfo.find_by_login_id(user.id)
            if not user_data:
                return {
                    "message": "Cannot find information associate with account."
                }, 500
            identity = {
                "login_id": user.id,
                "user_id": user_data.id
            }
            access_token = create_access_token(identity=identity, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)

            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200

        return {"message": "Invalid Credentials!"}, 401


class Register(Resource):
    def post(self):
        login_data = _user_login.parse_args()
        info_data = _user_info.parse_args()

        login_data["password"] = bcrypt.generate_password_hash(login_data["password"]).decode('utf8')
        user = UserLogin(**login_data)
        user.save_to_db()

        info_data["login_id"] = user.id
        info = UserInfo(**info_data)
        info.save_to_db()

        return {"message": "Account created successful"}, 200

    @jwt_required()
    def put(self):
        data = _user_login_edit.parse_args()
        identity = get_jwt_identity()
        user = UserLogin.find_by_id(identity["login_id"])

        if not user or user.username != data["username"]:
            return {"message": "Invalid request"}, 400

        if bcrypt.check_password_hash(user.password, data["password"]):
            user.password = bcrypt.generate_password_hash(data["new_password"]).decode('utf8')
            user.save_to_db()
            return {"message": "Password updated successfully"}, 200

        return {"message": "Invalid Credentials!"}, 401


class User(Resource):
    def __init__(self):
        verify_jwt_in_request()
        self.user_id = get_jwt_identity()["user_id"]

    def get(self):
        user = UserInfo.find_by_id(self.user_id)
        if user:
            return user.to_json(), 200

        return {"message": "User not found."}, 400

    def put(self):
        data = _user_info_edit.parse_args()
        user = UserInfo.find_by_id(self.user_id)
        if user:
            user.update(data)
            user.save_to_db()
            return {"message": "Information updated"}, 200

        return {"message": "User not found."}, 400




