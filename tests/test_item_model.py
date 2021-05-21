def test_model(item):
    assert item.name == "test_item"


def test_create_item(test_client, user_headers):
    res = test_client.post('api/items/new',
                           headers=user_headers,
                           json={
                               'name': "test_item2"
                           })

    assert res.status_code == 200


def test_delete_item(test_client, item, user_headers):
    res = test_client.delete(f'api/items/{item.id}',
                             headers=user_headers)

    assert res.status_code == 200
    assert res.get_json().get('message') == "Item deleted successfully"


def test_get_list_of_item(test_client, item, user_headers):
    res = test_client.get('api/items',
                          headers=user_headers)

    items_list = res.get_json()

    assert res.status_code == 200
    assert len(items_list) != 0
    assert items_list[0].get('name') == "test_item"


def test_send_item(test_client, host_user, item, user_headers):
    res = test_client.post('api/send',
                           headers=user_headers,
                           json={
                               'id': item.id,
                               'login': host_user.login
                           })

    assert res.status_code == 200
    assert res.get_json() == f"api/items/?login={host_user.login}&id={item.id}"


def test_get_item(test_client, host_user, item, host_user_headers):
    res = test_client.get('api/get',
                          headers=host_user_headers,
                          json={
                              'link': f"api/items/?login={host_user.login}&id={item.id}"
                          })

    assert res.status_code == 200


