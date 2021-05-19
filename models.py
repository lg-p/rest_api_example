from datetime import timedelta

from sqlalchemy import Column, Integer, String
from flask_jwt_extended import create_access_token
from passlib.hash import bcrypt

from app import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(250), nullable=False, unique=True)
    password = Column(String(120), nullable=False)

    def __init__(self, **kwargs):
        self.login = kwargs.get('login')
        self.password = bcrypt.hash(kwargs.get('password'))

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(identity=self.id, expires_delta=expire_delta)
        return token

    @classmethod
    def authenticate(cls, login, password):
        user = cls.query.filter(cls.login == login)
        if not bcrypt.verify(password, user.password):
            raise Exception("No user with this password")
        return user

    @classmethod
    def user_exists(cls, login: str) -> bool:
        """
        Checks for the existence of a user
        """
        user_exist = cls.query.filter(cls.login == login).scalar()
        return user_exist
