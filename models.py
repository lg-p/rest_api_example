from sqlalchemy import Column, Integer, String

from app import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(250), nullable=False, unique=True)
    password = Column(String(120), nullable=False)
