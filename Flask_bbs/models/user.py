import hashlib

from sqlalchemy import Column, String, Enum

import secret
from models.base_model import SQLMixin, db
from utils import log


class User(SQLMixin, db.Model):
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    image = Column(String(100), nullable=False, default='/images/default_avatar.png')
    signature = Column(String(100), nullable=False, default='Life is short, you need Python!')
    email = Column(String(50), nullable=False, default=secret.test_mail)
    role = Column(Enum('normal', 'admin'), nullable=False, default='normal')

    def is_admin(self):
        return self.role == 'admin'

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        salted = hashlib.sha256((password + salt).encode('ascii')).hexdigest()
        return salted

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        correct_password = form.get('re_password') == form.get('password')
        correct_name = len(name) > 2 and User.one(username=name) is None
        if correct_name and correct_password:
            form['password'] = User.salted_password(form['password'])
            u = User.new(form)
            return u
        else:
            log('register fail')
            return None

    @classmethod
    def validate_login(cls, form):
        query = dict(
            username=form['username'],
            password=User.salted_password(form['password']),
        )
        return User.one(**query)
