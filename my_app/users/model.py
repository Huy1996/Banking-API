from my_app.extensions import db


class UserModel(db.Model):
    __tablename__ = 'users'

    _id = db.Column(db.String(25), primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.INT, nullable=False)
    phone_number = db.Column(db.String(255), nullable=False, unique=True)
    pin = db.Column(db.String(9), nullable=False)

    def __init__(self, username, password, first_name, last_name, email, address, city, state, zip_code, phone_number, pin):
        self._username = username
        self._password = password
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._address = address
        self._city = city
        self._state = state
        self._zip_code = zip_code
        self._phone_number = phone_number
        self._pin = pin


