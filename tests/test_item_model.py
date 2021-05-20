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

