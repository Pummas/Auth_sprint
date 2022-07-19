from functools import wraps

import jwt
from core.config import app
from flask import request, jsonify

from .users import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(
                token, app.config['SECRET_KEY'],
                algorithms=["HS256"],
                verify_exp=True
            )
            current_user = User.query \
                .filter_by(id=data['id']) \
                .first()
        except jwt.ExpiredSignatureError:
            return jsonify({  # redirect to refresh
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)

    return decorated


def refresh_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'refresh-token' in request.headers:
            token = request.headers['refresh_token']
            return f(token, *args, **kwargs)
        return jsonify({
                'message': 'Refresh token is invalid !!'
            }), 401

    return decorated
