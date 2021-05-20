def test_model(item):
    assert item.name == "test_item"


def test_create_item(test_client, user_headers):
    res = test_client.post('api/items/new',
                           headers=user_headers,
                           json={
                               'name': "test_item2"
                           })

    assert res.status_code == 200
