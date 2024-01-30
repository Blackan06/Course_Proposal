from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from ..models.data_model import Course
from ..services.course_service import CourseService
from ..services.provider_service import ProviderService
from ..services.category_service import CategoryService
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
            'category': course.category,
            'course_image': CourseService.convert_image_to_base64(course.course_image),
        }
        for course in courses
    ]
    #return render_template('users/index.html', courses=courses_with_base64_images)
    return render_template('user_site/index.html', courses=courses_with_base64_images)

@user_controller.route('/search', methods=['POST'])
def search():
        input_name = request.form['coursename']

        courses = CourseService.search_course_by_name(input_name)

        print(courses)

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
        return render_template('user_site/result.html', courses=courses_with_base64_images)

@user_controller.route('/get_course_attribute', methods=['GET'])
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

        # courses_with_base64_images = [
        # {
        #     'course_id': course.course_id,
        #     'course_name': course.course_name,
        #     'course_description': course.course_description,
        #     'course_rate': course.course_rate,
        #     'course_path': course.course_path,         
        #     'provider': course.provider,  
        #     'category': course.category,
        #     'course_image': CourseService.convert_image_to_base64(course.course_image),
        # }
        # for course in courses
        # ]
        # return render_template('users/proposal.html', providers=providers, categories=categories, courses=courses_with_base64_images)
        return render_template('user_site/index.html', providers=providers, categories=categories, courses=courses_with_base64_images)

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

        return render_template('users/proposal.html', courses=courses_with_base64_images, providers=providers, categories=categories)
    
@user_controller.route('/get_course/<int:course_id>', methods=['GET'])
def get_course(course_id):
    try:
        course = Course.query.get(course_id)

        if not course:
            # Handle the case where the course with the given ID doesn't exist.
            return jsonify(error=f"Course with ID {course_id} not found"), 404

        providers = ProviderService.get_all_provider()
        categories = CategoryService.get_all_category()
        return render_template('user_site/course_detail.html', course=course, providers=providers, categories=categories)

    except ValueError as e:
        return jsonify(error=str(e)), 400

