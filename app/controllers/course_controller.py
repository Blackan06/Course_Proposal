from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from ..models.data_model import Course
from ..services.course_service import CourseService
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_login import login_required
course_controller = Blueprint('course_controller', __name__, url_prefix='/course')

@course_controller.route('/', methods=['GET'])
@course_controller.route('/index', methods=['GET'])
@login_required
def index():
    courses = CourseService.get_all_courses()
    return render_template('courses/index.html', courses=courses)

@course_controller.route('/create', methods=['POST'])
@login_required
def create():
    try:
        data = request.get_json()
        course_name = data.get('course_name')
        new_course = CourseService.create_course(course_name)
        return redirect(url_for('main.course_controller.index'))
    except Exception as e:
        return jsonify(error=str(e)), 400

@course_controller.route('/edit/<int:course_id>', methods=['POST'])
@login_required
def edit(course_id):
    try:
        course = Course.query.get(course_id)
        data = request.get_json()
        new_course_name = data.get('course_name')
        edited_course = CourseService.edit_course(course_id, new_course_name)
        return redirect(url_for('course_controller.index'))
    except Exception as e:
        return jsonify(error=str(e)), 400

@course_controller.route('/delete/<int:course_id>', methods=['DELETE'])
@login_required
def delete(course_id):
    try:
        success = CourseService.delete_course(course_id)
        if success:
            return redirect(url_for('course_controller.index'))
    except Exception as e:
        return jsonify(error=str(e)), 400
