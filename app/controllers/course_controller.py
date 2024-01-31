from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from ..models.data_model import Course, CourseProgrammingLanguage,ProgrammingLanguage
from ..services.course_service import CourseService
from ..services.provider_service import ProviderService
from ..services.category_service import CategoryService
from ..services.programming_language_service import ProgrammingLanguageService
from flask_login import login_required
course_controller = Blueprint('course_controller', __name__, url_prefix='/course')

@course_controller.route('/', methods=['GET'])
@course_controller.route('/index', methods=['GET'])
@login_required
def index():
    courses = CourseService.get_all_courses()
    if courses: 
        

        courses_with_base64_images = [
            {
                'course_id': course.course_id,
                'course_name': course.course_name,
                'course_description': course.course_description,
                'course_rate': course.course_rate,
                'course_path': course.course_path,         
                'provider': course.provider,  
                'category': course.category,
                'course_programming_languages': course.course_programming_languages,
                'course_image': CourseService.convert_image_to_base64(course.course_image),
            }
            for course in courses
        ]
        return render_template('courses/index.html', courses=courses_with_base64_images)
    return render_template('courses/index.html')
 
@course_controller.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    try:
        if request.method == 'POST':
            course_name = request.form['course_name']
            course_description = request.form['course_description']
            course_rate = request.form['course_rate']
            course_path = request.form['course_path']
            provider_id = request.form['provider_id']
            category_id = request.form['category_id']
            language_id = request.form.getlist('language_id')
            course_image = request.files['course_image']
            CourseService.create_course(
                course_name,
                course_description,
                course_rate,
                course_path,
                provider_id,
                category_id,
                language_id,
                course_image
            )
            return redirect(url_for('main.course_controller.index'))
        else:
            providers = ProviderService.get_all_provider()
            categories = CategoryService.get_all_category()
            languages = ProgrammingLanguageService.get_all_programming_language()
            return render_template('courses/create.html', providers=providers, categories=categories, languages=languages)

    except ValueError as e:
        return jsonify(error=str(e)), 400

@course_controller.route('/edit/<int:course_id>', methods=['GET', 'POST'])
@login_required
def edit(course_id):
    try:
        course = Course.query.get(course_id)

        if not course:
            # Handle the case where the course with the given ID doesn't exist.
            return jsonify(error=f"Course with ID {course_id} not found"), 404
        
        if request.method == 'POST':
            new_course_name = request.form['course_name']
            new_course_description = request.form['course_description']
            new_course_rate = request.form['course_rate']
            new_course_path = request.form['course_path']
            new_provider_id = request.form['provider_id']
            new_category_id = request.form['category_id']
            new_course_image = request.files['course_image']
            language_id = request.form.getlist('language_id[]')
            print(language_id)
            CourseService.edit_course(
                course_id,
                new_course_name,
                new_course_description,
                new_course_rate,
                new_course_path,
                new_provider_id,
                new_category_id,
                language_id,
                new_course_image
            )
            return redirect(url_for('main.course_controller.index'))
        else:
            languages = ProgrammingLanguageService.get_all_programming_language()
            selected_language_ids = [language.language_id for language in course.course_programming_languages]

            providers = ProviderService.get_all_provider()
            categories = CategoryService.get_all_category()
            return render_template('courses/edit.html', course=course, providers=providers, categories=categories,languages=languages,selected_language_ids=selected_language_ids)

    except ValueError as e:
        return jsonify(error=str(e)), 400

@course_controller.route('/delete/<int:course_id>', methods=['POST'])
@login_required
def delete(course_id):
    try:
        success = CourseService.delete_course(course_id)
       
    except Exception as e:
        return jsonify(error=str(e)), 400



@course_controller.route('/search', methods=['POST'])
def search():
        input_name = request.form['coursename']

        courses = CourseService.search_course_by_name(input_name)

        courses_with_base64_images = [
        {
             'course_id': course.course_id,
            'course_name': course.course_name,
            'course_description': course.course_description,
            'course_rate': course.course_rate,
            'course_path': course.course_path,         
            'provider': course.provider,  
            'category': course.category,
            'course_image': CourseService.convert_image_to_base64(course.course_image),
        }
        for course in courses
        ]
        return render_template('courses/index.html', courses=courses_with_base64_images)

@course_controller.route('/get_course_attribute', methods=['GET'])
def get_course_attribute():

        courses = CourseService.get_all_courses()

        courses_with_base64_images = [
        {
            'course_id': course.course_id,
            'course_name': course.course_name,
            'course_description': course.course_description,
            'course_rate': course.course_rate,
            'course_path': course.course_path,         
            'provider': course.provider,  
            'category': course.category,
            'course_image': CourseService.convert_image_to_base64(course.course_image),
        }
        for course in courses
        ]

        providers = ProviderService.get_all_provider()
        categories = CategoryService.get_all_category()

        return render_template('courses/index.html', providers=providers, categories=categories, courses=courses_with_base64_images)

@course_controller.route('/filter', methods=['GET','POST'])
def filter():
        category = request.form['categories']
        provider = request.form['providers']
        print(category)
        courses = CourseService.filter_courses(category=category, provider=provider)

        courses_with_base64_images = [
            {
                'course_name': course.course_name,
                'course_description': course.course_description,
                'course_rate': course.course_rate,
                'course_path': course.course_path,         
                'provider': course.provider,  
                'category': course.category,
                'course_image': CourseService.convert_image_to_base64(course.course_image),
            }
            for course in courses
        ]

        providers = ProviderService.get_all_provider()
        categories = CategoryService.get_all_category()

        return render_template('courses/index.html', courses=courses_with_base64_images, providers=providers, categories=categories)