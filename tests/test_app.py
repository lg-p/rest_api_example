from app import create_app


def test_client():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
