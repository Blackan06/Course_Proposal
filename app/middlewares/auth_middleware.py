from flask import request, jsonify
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity

def token_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        token = None

        # Thử lấy từ header Authorization
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        # Nếu không thành công, thử lấy từ cookie
        elif 'access_token' in request.cookies:
            token = request.cookies['access_token']

        if not token:
            return jsonify(message='Token is missing'), 401

        try:
            # Xác thực token
            current_user = get_jwt_identity()
        except:
            return jsonify(message='Token is invalid'), 401

        return fn(current_user, *args, **kwargs)

    return decorated
