from urllib import parse

from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_apispec import use_kwargs, marshal_with
from marshmallow import fields, validate

from app import session, docs
from app.items import bp_it
from models import Item, User
from schemes import ItemSchema


@bp_it.route('/items/new', methods=['POST'])
@jwt_required()
@use_kwargs(ItemSchema)
@marshal_with(ItemSchema)
def create_item(**kwargs):
    name = kwargs.get('name')

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
@use_kwargs(ItemSchema(only=('id',)))
@marshal_with(ItemSchema)
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
@marshal_with(ItemSchema(many=True))
def get_list_of_item():
    user_id = get_jwt_identity()

    items_list = Item.get_list_by_user(user_id)

    return items_list


@bp_it.route('/send', methods=['POST'])
@jwt_required()
@use_kwargs({'id': fields.Integer(), 'login': fields.String(required=True, validate=[validate.Length(max=250)])})
def send_item(**kwargs):
    user_id = get_jwt_identity()

    item_id = kwargs.get('id')
    host_user_login = kwargs.get('login')

    if not User.user_exists(host_user_login):
        raise Exception("User does not exist")

    item = Item.find_item(item_id, user_id)

    link = f"api/items/?login={host_user_login}&id={item.id}"

    return jsonify(link)


@bp_it.route('/get', methods=['GET'])
@jwt_required()
@use_kwargs({'link': fields.String(required=True)})
@marshal_with(ItemSchema)
def get_item(**kwargs):
    user_id = get_jwt_identity()

    link = kwargs.get('link')
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


docs.register(create_item, blueprint='it')
docs.register(delete_item, blueprint='it')
docs.register(get_list_of_item, blueprint='it')
docs.register(send_item, blueprint='it')
docs.register(get_item, blueprint='it')
