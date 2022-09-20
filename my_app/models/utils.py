import enum


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