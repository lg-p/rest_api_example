import pytest

from app import create_app


@pytest.fixture
def test_app():
    _app = create_app({
            'TESTING': True,
    })

    yield _app


@pytest.fixture
def test_client(test_app):
    return test_app.test_client()
