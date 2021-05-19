from flask import request, jsonify

from app.authentication import bp_auth
from models import User


@bp_auth.route('/login', methods=['POST'])
def authentication():
    param = request.json
    user_login = param.get('login')
    user_password = param.get('password')

    user = User.authenticate(user_login, user_password)
    token = user.get_token()

    return jsonify({
        'access_token': token
    })
