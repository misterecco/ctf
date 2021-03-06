# coding: utf-8
import flask_bcrypt as bcrypt

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship

from database import Base, db_session


class UserExists(Exception):
    pass


class UserDoesntExist(Exception):
    pass


class RegisterMixin(object):
    @classmethod
    def register(cls, *args, **kwargs):
        obj = cls(*args, **kwargs)
        db_session.add(obj)
        db_session.commit()
        return obj


class User(RegisterMixin, Base):
    is_authenticated = True
    is_active = True
    is_anonymous = False
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True)
    password = Column(String(50))
    public_key = Column(String(2000))  # Change size

    def __init__(self, username, password=None, public_key=None):
        super(User, self).__init__()
        self.username = username
        if password:
            password = bcrypt.generate_password_hash(password)
        self.password = password
        self.public_key = public_key

    def get_id(self):
        return self.id

    @staticmethod
    def load(user_id):
        return User.query.filter(User.id == user_id).first()

    @staticmethod
    def login(username, password):
        user = User.query.filter(User.username == username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        raise UserDoesntExist()

    @classmethod
    def register(cls, username, *args, **kwargs):
        username = username.strip().replace(' ', '').replace('\t', '')\
            .replace('\\', '').replace('/', '')
        try:
            return super(User, cls).register(username, *args, **kwargs)
        except IntegrityError:
            db_session.rollback()
            raise UserExists()


class Message(RegisterMixin, Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    encmessage = Column(String(5000))
    subject = Column(String(64))
    recipient_id = Column(Integer, ForeignKey('users.id'))
    sender_id = Column(Integer, ForeignKey('users.id'))
    sender = relationship('User', foreign_keys=[sender_id])

    def __init__(self, encmessage, subject, recipient_id, sender_id):
        super(Message, self).__init__()
        self.encmessage = encmessage
        self.subject = subject
        self.recipient_id = recipient_id
        self.sender_id = sender_id
