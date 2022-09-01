from my_app.models.base import db, Base, UUID


class Transaction(Base):
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

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def to_json(self):
        return {
            "id": self.id,
            "transaction_amount": self.transaction_amount,
            "account_id": self.account_id,
            "receiver": self.receiver,
            "checking_image": self.check_image,
            "comment": self.comment
        }

