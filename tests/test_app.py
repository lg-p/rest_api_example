from app import create_app
from config import TestConfig


def test_client():
    assert not create_app().testing
    assert create_app(test_config=TestConfig).testing
