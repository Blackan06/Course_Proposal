from flask import Flask , render_template,url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from .routes import main
from .services.user_service import  User
from flask_login import LoginManager
from sqlalchemy.exc import SQLAlchemyError
from .models.data_model import db,Course
from flask_migrate import Migrate
from functools import wraps
from .services.course_service import CourseService
from .services.provider_service import ProviderService
from .services.category_service import CategoryService
from .services.programming_language_service import ProgrammingLanguageService


def create_app():
    app = Flask(__name__)
    login_manager = LoginManager(app)

    # Load biến môi trường từ file .env
    load_dotenv()

    # Cấu hình SQLAlchemy trực tiếp
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    # Cấu hình token
    app.config['SECRET_KEY'] = f"{os.getenv('SECRET_KEY')}"

    

    # Cấu hình SQLAlchemy cho models
    db.init_app(app)

    
    
    @login_manager.user_loader
    def load_user(user_id):
        username = os.getenv('USER_NAME')
        password = os.getenv('PASS_WORD')
        user_name = str(username)
        print(user_id + ' userId')
        print( user_name + ' userId')
        # Validate user credentials
        if user_id == username:
            print('User have')
            return User(user_id=username, username=username, password=password)

        return None

    migrate = Migrate(app, db)

    app.register_blueprint(main)

    @app.route('/')
    @app.route('/index', methods=['GET'])
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
        providers = ProviderService.get_all_provider()
        categories = CategoryService.get_all_category()
        programming_languages = ProgrammingLanguageService.get_all_programming_language()
        print(categories)
        #return render_template('users/index.html', courses=courses_with_base64_images)
        return render_template('user_site/index.html', courses=courses_with_base64_images, providers=providers, categories=categories, 
                                                        programming_languages=programming_languages)

    return app
