from sqlalchemy import Column, Integer, String

from models.base_model import db, SQLMixin
from models.user import User


class Token(SQLMixin, db.Model):
    content = Column(String(36), nullable=False)
    user_id = Column(Integer, nullable=True)

    def user(self):
        u = User.one(id=self.user_id)
        return u
