from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from ..models.data_model import Course
from ..services.course_service import CourseService
from ..services.provider_service import ProviderService
from ..services.category_service import CategoryService
from ..services.programming_language_service import ProgrammingLanguageService
from ..services.user_service import UserService
user_controller = Blueprint('user_controller', __name__, url_prefix='/user')

@user_controller.route('/', methods=['GET'])
@user_controller.route('/index', methods=['GET'])
def index():
    courses = CourseService.get_all_courses()
    courses_with_base64_images = [
        {
            'course_id': course.course_id,
            'course_name': course.course_name,
            'course_description': course.course_description,
            'course_rate': course.course_rate,
            'course_path': course.course_path,         
            'provider': course.provider,  
            'course_programming_languages': course.course_programming_languages,
            'course_image': CourseService.convert_image_to_base64(course.course_image),
            'category': course.category,
        }
        for course in courses
    ]
    providers = ProviderService.get_all_provider()
    categories = CategoryService.get_all_category()
    programming_languages = ProgrammingLanguageService.get_all_programming_language()
    print(categories)
    #return render_template('users/index.html', courses=courses_with_base64_images)
    return render_template('user_site/index.html', courses=courses_with_base64_images, providers=providers, categories=categories, 
                                                    programming_languages=programming_languages)

@user_controller.route('/search', methods=['POST'])
def search():
        input_name = request.form['coursename']
        category = request.form['categories']
        provider = request.form['providers']
        programming_languages = request.form['programming_languages']

        print("category", category)
        print("Provider", provider)

        courses = CourseService.search_course_by_name(input_name=input_name, category=category, provider=provider, programming_language=programming_languages)

        # print('courses is here')

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
        # return render_template('users/index.html', courses=courses_with_base64_images)
        providers = ProviderService.get_all_provider()
        categories = CategoryService.get_all_category()
        programming_language = ProgrammingLanguageService.get_all_programming_language()
        return render_template('user_site/result.html', courses=courses_with_base64_images, providers=providers, categories=categories, 
                                                    programming_language=programming_language)

@user_controller.route('/get_course_attribute', methods=['GET'])
def get_course_attribute():
        
        courses = CourseService.get_all_courses()
        
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
        programing_languages = ProgrammingLanguageService.get_all_programming_language()
        return render_template('user_site/index.html', providers=providers, categories=categories, courses=courses_with_base64_images, 
                                                    programing_languages=programing_languages)

@user_controller.route('/filter', methods=['GET','POST'])
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
        programing_languages = ProgrammingLanguageService.get_all_programming_language()
        return render_template('users/proposal.html', courses=courses_with_base64_images, providers=providers, categories=categories,
                                                        programing_languages=programing_languages)
    
@user_controller.route('/get_course/<int:course_id>', methods=['GET'])
def get_course(course_id):
    try:
        course = Course.query.get(course_id)

        if not course:
            # Handle the case where the course with the given ID doesn't exist.
            return jsonify(error=f"Course with ID {course_id} not found"), 404

        course_with_base64_images = {
            'course_id': course.course_id,
            'course_name': course.course_name,
            'course_description': course.course_description,
            'course_rate': course.course_rate,
            'course_path': course.course_path,         
            'provider': course.provider,  
            'course_programming_languages': course.course_programming_languages,
            'course_image': CourseService.convert_image_to_base64(course.course_image),
            'category': course.category, 
        }

        providers = ProviderService.get_all_provider()
        categories = CategoryService.get_all_category()

        return render_template('user_site/course_detail.html', course=course_with_base64_images, providers=providers, categories=categories)

    except ValueError as e:
        return jsonify(error=str(e)), 400
