from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from ..models.data_model import CourseProgrammingLanguage
from ..services.course_programming_language_service import CourseProgrammingLanguageService
from ..services.course_service import CourseService
from ..services.programming_language_service import ProgrammingLanguageService
from flask_login import login_required
course_programming_language_controller = Blueprint('course_programming_language_controller', __name__, url_prefix='/courseprogramminglanguage')

@course_programming_language_controller.route('/', methods=['GET'])
@course_programming_language_controller.route('/index', methods=['GET'])
@login_required
def index():
    course_programming_languages = CourseProgrammingLanguageService.get_all_course_programming_language()
    return render_template('course_programming_languages/index.html', course_programming_languages=course_programming_languages)

@course_programming_language_controller.route('/create', methods=['GET','POST'])
@login_required
def create():
    try:
        if request.method == 'POST':
            course_id = request.form['course_id']
            language_id = request.form['language_id']
            CourseProgrammingLanguageService.create_course_programming_language(course_id,language_id)
            return redirect(url_for('main.course_programming_language_controller.index'))
        else:
            courses = CourseService.get_all_courses()
            programming_languages = ProgrammingLanguageService.get_all_programming_language()
            return render_template('course_programming_languages/create.html', courses = courses, programming_languages = programming_languages)
    except Exception as e:
        return jsonify(error=str(e)), 400

@course_programming_language_controller.route('/edit/<int:course_programming_language_id>', methods=['GET','POST'])
@login_required
def edit(course_programming_language_id):
    try:
        if request.method == 'POST':
            course_programming_language = CourseProgrammingLanguageService.get_course_programming_language_by_id(course_programming_language_id)
            new_course_id = request.form['course_id']
            new_language_id = request.form['language_id']
            CourseProgrammingLanguageService.edit_course_programming_language(course_programming_language_id, new_course_id,new_language_id)
            return redirect(url_for('main.course_programming_language_controller.index'))
        else:
            courses = CourseService.get_all_courses()
            programming_languages = ProgrammingLanguageService.get_all_programming_language()
            return render_template('course_programming_languages/edit.html',courses = courses, programming_languages = programming_languages)
    except Exception as e:
        return jsonify(error=str(e)), 400

@course_programming_language_controller.route('/delete/<int:course_programming_language_id>', methods=['DELETE'])
@login_required
def delete(course_programming_language_id):
    try:
        success = ProgrammingLanguageService.delete_programming_language(course_programming_language_id)
        
    except Exception as e:
        return jsonify(error=str(e)), 400
