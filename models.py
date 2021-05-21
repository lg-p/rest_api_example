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
        result = cls.query.filter(cls.login == login)
        if not result.scalar():
            raise Exception("No user with this login")

        user = result.one()
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

    @classmethod
    def find_user_by_login(cls, login: str):
        """
        Searches for an user by login
        :return: User
        """
        res = cls.query.filter(cls.login == login)

        if not res.scalar():
            raise Exception("User not found")

        return res.one()


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
        res = cls.query.filter(cls.id == item_id, cls.user_id == user_id)
        if not res.scalar():
            raise Exception("Item not found")

        return res.one()

    @classmethod
    def find_item_by_id(cls, item_id: int):
        """
        Searches for an item by id
        :return: Item
        """
        res = cls.query.filter(cls.id == item_id)
        if not res.scalar():
            raise Exception("Item not found")

        return res.one()

    @classmethod
    def get_list_by_user(cls, user_id: int) -> list:
        """
        Gets a list of items for a specific user
        """
        items_list = []

        result = cls.query.filter(cls.user_id == user_id).all()
        for item in result:
            items_list.append({
                    'id': item.id,
                    'name': item.name
                })

        return items_list
