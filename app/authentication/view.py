from flask import jsonify
from flask_apispec import use_kwargs, marshal_with

from app.authentication import bp_auth
from models import User
from schemes import UserSchema, AuthenticationSchema


@bp_auth.route('/login', methods=['POST'])
@use_kwargs(UserSchema)
@marshal_with(AuthenticationSchema)
def authentication(**kwargs):
    user_login = kwargs.get('login')
    user_password = kwargs.get('password')

    user = User.authenticate(user_login, user_password)
    token = user.get_token()

    return jsonify({
        'access_token': token
    })
