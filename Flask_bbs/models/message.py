from sqlalchemy import Column, Unicode, UnicodeText, Integer

from models.base_model import SQLMixin, db
from models.user import User


class Messages(SQLMixin, db.Model):
    title = Column(Unicode(50), nullable=False)
    content = Column(UnicodeText, nullable=False)
    sender_id = Column(Integer, nullable=False)
    receiver_id = Column(Integer, nullable=False)

    def sender(self):
        return User.one(id=self.sender_id)

    def receiver(self):
        return User.one(id=self.receiver_id)
