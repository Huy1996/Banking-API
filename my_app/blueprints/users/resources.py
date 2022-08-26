from flask_restful import Resource, reqparse

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

_user_info = reqparse.RequestParser()
_user_info.add_argument('first_name', **str_require)
_user_info.add_argument('last_name', **str_require)
_user_info.add_argument('email', **str_require)
_user_info.add_argument('address', **str_require)
_user_info.add_argument('city', **str_require)
_user_info.add_argument('state', **str_require)
_user_info.add_argument('zip_code', **int_require)
_user_info.add_argument('pin', **str_require)


class Login(Resource):
    def post(self):
        pass


class Register(Resource):
    def post(self):
        pass

