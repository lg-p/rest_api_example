from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import session
from app.items import bp_it
from models import Item


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

