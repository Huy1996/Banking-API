import enum

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test123@localhost:5433/banking'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)


class Abstract(db.Model):
    __abstract__ = True

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class AbstractModel(Abstract):
    __abstract__ = True

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()


class UserLogin(AbstractModel):
    __tablename__ = 'user_login'

    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    info = db.relationship('UserInfo', backref="user_login")

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()


class UserInfo(AbstractModel):
    __tablename__ = 'user_info'

    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    login_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user_login.id'))
    account = db.relationship('Account', backref="user_info")

    def __init__(self, first_name, last_name, email, login_id):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.login_id = login_id

    @classmethod
    def find_by_login_id(cls, _id):
        return cls.query.filter_by(login_in=_id).first()


class AccountType(enum.Enum):
    CHECKING = 'Checking'
    SAVING = 'Saving'


class AccountStatus(enum.Enum):
    OPENED = 1
    CLOSED = -1


class Account(AbstractModel):
    __tablename__ = "account"

    account_type = db.Column(db.Enum(AccountType,
                                     values_callable=lambda x: [str(member.value) for member in AccountType]),
                             nullable=False)
    balance = db.Column(db.DECIMAL, nullable=False, default=0)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user_info.id'), nullable=False)
    account_status = db.Column(db.Enum(AccountStatus,
                                       values_callable=lambda x: [str(member.value) for member in
                                                                  AccountStatus]),
                               nullable=False, default=AccountStatus.OPENED)

    def __init__(self, _type, user_id):
        self.account_type = _type
        self.user_id = user_id



# from playground import UserLogin, UserInfo, Account, AccountType, db
# db.drop_all()
# db.create_all()
# user_login = UserLogin("alex", "test123")
# user_login.save_to_db()
# user_info = UserInfo("alex", "noir", "alex@example.com", user_login.id)
# user_info.save_to_db()
# account = Account(AccountType["CHECKING"], user_info.id)
# account.save_to_db()