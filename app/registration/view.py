from flask import jsonify
from flask_apispec import use_kwargs, marshal_with
from sqlalchemy.exc import SQLAlchemyError

from app.registration import bp_reg
from models import User
from app import docs, logger, db
from schemes import UserSchema


@bp_reg.route('/registration', methods=['POST'])
@use_kwargs(UserSchema)
@marshal_with(UserSchema)
def registration(**kwargs):
    user_login = kwargs.get('login')

    if User.user_exists(user_login):
        return jsonify({
            'message': "User with this login already exists"
        })

    user = User(**kwargs)
    try:
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError as errors:
        logger.exception(f'User registration failed: {errors.args[0]}')
        return jsonify({
            'message': "User registration failed"
        })

    return jsonify({
        'message': "User registered successfully"
    })


docs.register(registration, blueprint='reg')
