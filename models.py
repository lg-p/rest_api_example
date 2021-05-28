from datetime import timedelta

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_jwt_extended import create_access_token
from passlib.hash import bcrypt

from app import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(250), nullable=False, unique=True)
    password = Column(String(120), nullable=False)
    items = relationship('Item')

    def __init__(self, **kwargs):
        self.login = kwargs.get('login')
        self.password = bcrypt.hash(kwargs.get('password'))

    def get_token(self, expire_time=24) -> str:
        """
        Creates an access token
        """
        expire_delta = timedelta(expire_time)
        token = create_access_token(identity=self.id, expires_delta=expire_delta)
        return token

    @classmethod
    def authenticate(cls, login: str, password: str):
        """
        User authentication
        """
        user = cls.query.filter(cls.login == login).one()

        if not bcrypt.verify(password, user.password):
            raise UserException("Invalid password")

        return user

    @classmethod
    def user_exists(cls, login: str) -> bool:
        """
        Checks for the existence of a user
        """
        user_exist = cls.query.filter(cls.login == login).scalar()
        return user_exist

    @classmethod
    def find_user_by_login(cls, login: str):
        """
        Searches for an user by login
        :return: User
        """
        user = cls.query.filter(cls.login == login).one()

        return user


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, nullable=True, primary_key=True)
    name = Column(String(250), nullable=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    @classmethod
    def item_exists(cls, name: str, user_id: str) -> bool:
        """
        Checks for the existence of a item
        """
        item_exist = cls.query.filter(cls.name == name, cls.user_id == user_id).scalar()
        return item_exist

    @classmethod
    def find_item(cls, item_id: int, user_id: int):
        """
        Searches for an item by id
        :return: Item
        """
        item = cls.query.filter(cls.id == item_id, cls.user_id == user_id).one()

        return item

    @classmethod
    def find_item_by_id(cls, item_id: int):
        """
        Searches for an item by id
        :return: Item
        """
        item = cls.query.filter(cls.id == item_id).one()

        return item

    @classmethod
    def get_list_by_user(cls, user_id: int) -> list:
        """
        Gets a list of items for a specific user
        """
        result = cls.query.filter(cls.user_id == user_id).all()

        return result


class UserException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
