from flask import jsonify
from flask_apispec import use_kwargs, marshal_with
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from app import docs, logger
from app.authentication import bp_auth
from models import User, UserException
from schemes import UserSchema, AuthenticationSchema


@bp_auth.route('/login', methods=['POST'])
@use_kwargs(UserSchema)
@marshal_with(AuthenticationSchema)
def authentication(**kwargs):
    user_login = kwargs.get('login')
    user_password = kwargs.get('password')

    try:
        user = User.authenticate(user_login, user_password)
        token = user.get_token()
    except (MultipleResultsFound, NoResultFound) as errors:
        logger.exception(f'User authentication failed: {errors.args[0]}')
        return jsonify({
            'message': "Invalid user"
        })
    except UserException as error_message:
        return jsonify({
            'message': error_message
        })
    except Exception as error_message:
        logger.exception(f'User authentication failed: {error_message}')
        return jsonify({
            'message': error_message
        })

    return jsonify({
        'access_token': token
    })


docs.register(authentication, blueprint='auth')
