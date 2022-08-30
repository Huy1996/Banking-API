from uuid import uuid4
from my_app.extensions import db
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


class Base(db.Model):
    __abstract__ = True

    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class AbstractId(Base):
    __abstract__ = True

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
