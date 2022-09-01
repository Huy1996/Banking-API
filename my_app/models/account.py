import enum
from my_app.models.base import db, AbstractId, UUID
from my_app.models.transaction import Transaction
from datetime import datetime


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


class Account(AbstractId):
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