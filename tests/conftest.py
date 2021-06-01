import pytest

from app import create_app, db
from models import User, Item
from config import TestConfig


@pytest.fixture
def test_app():
    _app = create_app(test_config=TestConfig)

    yield _app


@pytest.fixture
def test_client(test_app):
    return test_app.test_client()


@pytest.fixture
def session(test_app):
    ctx = test_app.app_context()
    ctx.push()
    db.create_all()

    yield db.session

    db.session.remove()
    db.drop_all()
    ctx.pop()


@pytest.fixture
def user(session):
    user = User(login="test_user", password="password")
    session.add(user)
    session.commit()

    return user


@pytest.fixture
def host_user(session):
    user = User(login="host_user", password="password")
    session.add(user)
    session.commit()

    return user


@pytest.fixture
def item(user, session):
    item = Item(name="test_item", user_id=user.id)
    session.add(item)
    session.commit()
    return item


@pytest.fixture
def user_token(user, test_client):
    res = test_client.post('/api/login',
                           json={
                               'login': "test_user",
                               'password': "password"
                           })

    return res.get_json()['access_token']


@pytest.fixture
def user_headers(user_token):
    headers = {
        'Authorization': f"Bearer {user_token}"
    }

    return headers


@pytest.fixture
def host_user_token(user, test_client):
    res = test_client.post('/api/login',
                           json={
                               'login': "host_user",
                               'password': "password"
                           })

    return res.get_json()['access_token']


@pytest.fixture
def host_user_headers(host_user_token):
    headers = {
        'Authorization': f"Bearer {host_user_token}"
    }

    return headers
