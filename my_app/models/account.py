import enum
from my_app.models.base import db, AbstractId, UUID
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

    def __init__(self, _type, user_id):
        self.account_type = _type
        self.user_id = user_id

    def transfer_to(self, account_id, amount):
        if self.balance < amount:
            # TODO: Create transaction with reject code
            pass

        target = Account.find_by_id(account_id)
        if target:
            # TODO: Create Transaction with reject code
            pass

        self.balance -= amount
        target.balance += amount
        # TODO: Create Transaction with transfer code
        self.save_to_db()
        target.save_to_db()

    def deposit(self, amount):
        # TODO: Implement deposit function
        pass

    def withdraw(self, amount):
        # TODO: Implement withdraw function
        pass

    def confirmation_code(self, code):
        dt_str = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        return f'{code.value}-{str(self.id)[-4:]}-{dt_str}'






