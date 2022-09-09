from my_app.models.base import db, AbstractId, UUID


class UserLogin(AbstractId):
    __tablename__ = 'user_login'

    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()


class UserInfo(AbstractId):
    __tablename__ = 'user_info'

    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(255), nullable=False, unique=True)
    pin = db.Column(db.String(9), nullable=False)
    login_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user_login.id'))

    def __init__(self, first_name, last_name, email, address, city, state, zip_code, phone_number, pin, login_id):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone_number = phone_number
        self.pin = pin
        self.login_id = login_id

    @classmethod
    def find_by_login_id(cls, _id):
        return cls.query.filter_by(login_id=_id).first()

    def update(self, new_data):
        for key, value in new_data.items():
            getattr(self, key)
            setattr(self, key, value)

    def to_json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "phone_number": self.phone_number,
        }