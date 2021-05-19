import pytest
from sqlalchemy.orm.session import close_all_sessions

from app import create_app, Base, engine, session as db_session
from models import User


@pytest.fixture
def test_app():
    _app = create_app({
            'TESTING': True,
    })

    Base.metadata.create_all(bind=engine)
    _app.connection = engine.connect()

    yield _app

    Base.metadata.drop_all(bind=engine)
    _app.connection.close()


@pytest.fixture
def test_client(test_app):
    return test_app.test_client()


@pytest.fixture
def session(test_app):
    ctx = test_app.app_context()
    ctx.push()

    yield db_session

    close_all_sessions()
    ctx.pop()


@pytest.fixture
def user(session):
    user = User(login="test_user", password="password")
    session.add(user)
    session.commit()

    return user



