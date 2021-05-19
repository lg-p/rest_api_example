from flask import request, jsonify

from app.registration import bp_reg
from models import User
from app import session


@bp_reg.route('/registration', methods=['POST'])
def registration():
    param = request.json
    user_login = param.get('login')

    if User.user_exists(user_login):
        raise Exception("User with this login already exists")

    user = User(**param)
    try:
        session.add(user)
        session.commit()
    except Exception as e:
        return jsonify({
            'message': e
        })

    return jsonify({
        'message': 'User registered successfully'
    })