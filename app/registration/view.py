from flask import jsonify
from flask_apispec import use_kwargs, marshal_with

from app.registration import bp_reg
from models import User
from app import session, docs
from schemes import UserSchema


@bp_reg.route('/registration', methods=['POST'])
@use_kwargs(UserSchema)
@marshal_with(UserSchema)
def registration(**kwargs):
    user_login = kwargs.get('login')

    if User.user_exists(user_login):
        raise Exception("User with this login already exists")

    user = User(**kwargs)
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


docs.register(registration, blueprint='reg')
