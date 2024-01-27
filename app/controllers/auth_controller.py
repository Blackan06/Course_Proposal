from flask import Blueprint, render_template, request, jsonify
from flask_login import login_user, logout_user, login_required
from ..services.user_service import UserService
from datetime import timedelta

auth_controller = Blueprint('auth_controller', __name__, url_prefix='/auth')

@auth_controller.route('/login', methods=['GET'])
def login_page():
    return render_template('auth/login.html')
@auth_controller.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = UserService.load_user(username)

        if user and password == user.password:
            login_user(user)
            print(user.username)
            return jsonify(message='Logged in successfully'), 200

    return jsonify(message='Invalid credentials'), 401


@auth_controller.route('/protected', methods=['GET'])
@login_required
def protected():
    try:
        return jsonify(message='ok'), 200
    except Exception as e:
        print(f"Error processing protected route: {e}")
        return jsonify(message='Unauthorized'), 401



@auth_controller.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify(message='Logged out successfully'), 200
