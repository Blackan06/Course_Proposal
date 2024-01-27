from flask import Blueprint
from .controllers.course_controller import course_controller
from .controllers.auth_controller import auth_controller

main = Blueprint('main', __name__)

main.register_blueprint(auth_controller)
main.register_blueprint(course_controller)
