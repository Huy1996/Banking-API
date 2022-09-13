import enum

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import datetime

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
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

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


class TransactionCode(enum.Enum):
    DEPOSIT = "D"
    WITHDRAW = "W"
    TRANSFER = "T"
    REJECTED = "X"
    RECEIVED = "R"


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
    transactions = db.relationship("Transaction", backref="account")

    def __init__(self, _type, user_id):
        self.account_type = _type
        self.user_id = user_id

    def transfer(self, account_id, amount):
        self.__validate_balance(amount)

        target = Account.__find_receiver(account_id)

        self.balance -= amount
        self.save_to_db()

        target.receive(amount)
        return self.__transaction_record(TransactionCode.TRANSFER, amount, target.id)

    def __validate_balance(self, amount):
        if self.balance < amount:
            self.__transaction_record(TransactionCode.REJECTED,
                                      amount,
                                      comment="Insufficient amount: Your balance not enough to make this "
                                              "transaction. "
                                      )
            raise ValueError("Insufficient amount: Your balance not enough to make this transaction.")

    @classmethod
    def __find_receiver(cls, account_id):
        receiver = cls.find_by_id(account_id)
        if not receiver or receiver.account_status == AccountStatus.CLOSED:
            raise Warning("Account is not exist or inactive")
        return receiver

    def receive(self, amount):
        self.balance += amount
        self.save_to_db()
        self.__transaction_record(TransactionCode.RECEIVED, amount)

    def deposit(self, amount, check_image):
        if amount <= 0:
            raise ValueError("Invalid amount.")
        self.balance += amount
        self.save_to_db()
        return self.__transaction_record(TransactionCode.DEPOSIT, amount, check_image=check_image)

    def withdraw(self, amount):
        self.__validate_balance(amount)
        self.balance -= amount
        self.save_to_db()
        return self.__transaction_record(TransactionCode.WITHDRAW, amount)

    def __transaction_record(self, code, amount, receiver=None, check_image=None, comment=""):
        _id = self.confirmation_code(code.value)
        transaction = Transaction(_id, amount, self.id, receiver, check_image, comment)
        transaction.save_to_db()
        return transaction

    def confirmation_code(self, code):
        dt_str = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        return f'{code}-{str(self.id)[-12:]}-{dt_str}'

    def to_json(self):
        return {
            "id": self.id,
            "type": self.account_type.value,
            "balance": self.balance,
            "user_id": self.user_id,
        }


class Transaction(Abstract):
    __tablename__ = "transaction"

    id = db.Column(db.String(255), nullable=False, unique=True, primary_key=True)
    transaction_amount = db.Column(db.DECIMAL, nullable=False)
    account_id = db.Column(UUID(as_uuid=True), db.ForeignKey('account.id'), nullable=False)
    receiver = db.Column(UUID(as_uuid=True), nullable=True)
    check_image = db.Column(db.String(255), nullable=True)
    comment = db.Column(db.String(255))

    def __init__(self, _id, amount, sender, receiver=None, check_image=None, comment=""):
        self.id = _id
        self.transaction_amount = amount
        self.account_id = sender
        self.receiver = receiver
        self.check_image = check_image
        self.comment = comment

    def to_json(self):
        return {
            "id": self.id,
            "transaction_amount": self.transaction_amount,
            "account_id": self.account_id,
            "receiver": self.receiver,
            "checking_image": self.check_image,
            "comment": self.comment
        }

# from playground import UserLogin, UserInfo, Account, AccountType,

from pprint import PrettyPrinter

printer = PrettyPrinter().pprint

# db.drop_all()
# db.create_all()
# alex_login = UserLogin("alex", "test123")
# alex_login.save_to_db()
# alex_info = UserInfo("alex", "noir", "alex@example.com", alex_login.id)
# alex_info.save_to_db()
# alex_checking = Account(AccountType.CHECKING, alex_info.id)
# alex_checking.save_to_db()
# alex_saving = Account(AccountType.SAVING, alex_info.id)
# alex_saving.save_to_db()

