from urllib import parse

from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_apispec import use_kwargs, marshal_with
from sqlalchemy.exc import SQLAlchemyError, MultipleResultsFound, NoResultFound

from app import session, docs, logger
from app.items import bp_it
from models import Item, User
from schemes import ItemSchema, SendItemSchema, URLSchema


@bp_it.route('/items/new', methods=['POST'])
@jwt_required()
@use_kwargs(ItemSchema)
@marshal_with(ItemSchema)
def create_item(**kwargs):
    name = kwargs.get('name')

    user_id = get_jwt_identity()
    if Item.item_exists(name, user_id):
        return jsonify({
            'message': "Item  with this name already exists"
        })

    item = Item(name=name, user_id=user_id)
    try:
        session.add(item)
        session.commit()
    except SQLAlchemyError as errors:
        logger.exception(f'Failed to create item: {errors.args[0]}')
        return jsonify({
            'message': "Failed to create item"
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

    try:
        item = Item.find_item(int(item_id), user_id)
        session.delete(item)
        session.commit()
    except (MultipleResultsFound, NoResultFound) as errors:
        logger.exception(f'Item not found: {errors.args[0]}')
        return jsonify({
            'message': "Item not found"
        })
    except SQLAlchemyError as errors:
        logger.exception(f'Failed to delete item: {errors.args[0]}')
        return jsonify({
            'message': "Failed to delete item"
        })

    return jsonify({
        'message': "Item deleted successfully"
    })


@bp_it.route('/items', methods=['GET'])
@jwt_required()
@marshal_with(ItemSchema(many=True))
def get_list_of_item():
    user_id = get_jwt_identity()

    try:
        items_list = Item.get_list_by_user(user_id)
        return items_list
    except SQLAlchemyError as errors:
        logger.exception(f'Failed to get the list of items: {errors.args[0]}')
        return jsonify([{
            'message': "Failed to get the list of items"
        }])


@bp_it.route('/send', methods=['POST'])
@jwt_required()
@use_kwargs(SendItemSchema)
@marshal_with(URLSchema)
def send_item(**kwargs):
    user_id = get_jwt_identity()

    item_id = kwargs.get('id')
    host_user_login = kwargs.get('login')

    if not User.user_exists(host_user_login):
        return jsonify({
            'message': "User does not exist"
        })

    try:
        item = Item.find_item(item_id, user_id)
    except SQLAlchemyError as errors:
        logger.exception(f'Failed to find item: {errors.args[0]}')
        return jsonify({
            'message': "Failed to find item"
        })

    link = f"api/items/?login={host_user_login}&id={item.id}"

    return jsonify(link)


@bp_it.route('/get', methods=['GET'])
@jwt_required()
@use_kwargs(URLSchema)
@marshal_with(ItemSchema)
def get_item(**kwargs):
    user_id = get_jwt_identity()

    link = kwargs.get('link')
    parsed_query = parse.urlparse(link).query
    parsed_params = parse.parse_qsl(parsed_query)

    user_login = str(parsed_params[0][1])
    item_id = int(parsed_params[1][1])

    try:
        user = User.find_user_by_login(user_login)
    except SQLAlchemyError as errors:
        logger.exception(f'Failed to find user: {errors.args[0]}')
        return jsonify({
            'message': "Failed to find user"
        })

    if user_id != user.id:
        return jsonify({
            'message': "The link is for another user"
        })

    try:
        item = Item.find_item_by_id(item_id)
        item.user_id = user.id
        session.add(item)
        session.commit()
    except SQLAlchemyError as errors:
        logger.exception(f'Failed to update item: {errors.args[0]}')
        return jsonify({
            'message': "Failed to update item"
        })

    return jsonify({
        'message': "Item received successfully"
    })


docs.register(create_item, blueprint='it')
docs.register(delete_item, blueprint='it')
docs.register(get_list_of_item, blueprint='it')
docs.register(send_item, blueprint='it')
docs.register(get_item, blueprint='it')
