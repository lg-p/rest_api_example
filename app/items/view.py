from urllib import parse

from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import session
from app.items import bp_it
from models import Item, User


@bp_it.route('/items/new', methods=['POST'])
@jwt_required()
def create_item():
    param = request.json
    name = param.get('name')

    user_id = get_jwt_identity()
    if Item.item_exists(name, user_id):
        raise Exception("Item  with this name already exists")

    item = Item(name=name, user_id=user_id)
    try:
        session.add(item)
        session.commit()
    except Exception as e:
        return jsonify({
            'message': e
        })

    return jsonify({
        'message': f"Item created successfully, {item.id}, {item.name}"
    })


@bp_it.route('/items/<item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    user_id = get_jwt_identity()

    item = Item.find_item(int(item_id), user_id)

    try:
        session.delete(item)
        session.commit()
    except Exception as e:
        return jsonify({
            'message': e
        })

    return jsonify({
        'message': "Item deleted successfully"
    })


@bp_it.route('/items', methods=['GET'])
@jwt_required()
def get_list_of_item():
    user_id = get_jwt_identity()

    items_list = Item.get_list_by_user(user_id)

    return jsonify(items_list)


@bp_it.route('/send', methods=['POST'])
@jwt_required()
def send_item():
    user_id = get_jwt_identity()

    param = request.get_json()
    item_id = param.get('id')
    host_user_login = param.get('login')

    if not User.user_exists(host_user_login):
        raise Exception("User does not exist")

    item = Item.find_item(item_id, user_id)

    link = f"api/items/?login={host_user_login}&id={item.id}"

    return jsonify(link)


@bp_it.route('/get', methods=['GET'])
@jwt_required()
def get_item():
    user_id = get_jwt_identity()

    link = request.get_json().get('link')
    parsed_query = parse.urlparse(link).query
    parsed_params = parse.parse_qsl(parsed_query)

    user_login = str(parsed_params[0][1])
    item_id = int(parsed_params[1][1])

    user = User.find_user_by_login(user_login)
    if user_id != user.id:
        raise Exception("The link is for another user")

    item = Item.find_item_by_id(item_id)

    try:
        item.user_id = user.id
        session.add(item)
        session.commit()
    except Exception as e:
        return jsonify({
            'message': e
        })

    return jsonify({
        'message': "Item received successfully"
    })
