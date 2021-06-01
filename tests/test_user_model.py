def test_model(user):
    assert user.login == "test_user"


def test_registration(user, test_client):
    res = test_client.post('/api/registration',
                           json={
                               'login': "test_user2",
                               'password': "password"
                           })
    assert res.status_code == 200
    assert res.get_json().get('message') == "User registered successfully"


def test_authentication(user, test_client):
    res = test_client.post('/api/login',
                           json={
                               'login': "test_user",
                               'password': "password"
                           })

    assert res.status_code == 200
    assert res.get_json().get('access_token')
