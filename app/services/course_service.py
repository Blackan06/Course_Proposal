from ..services.category_service import CategoryService
from ..services.provider_service import ProviderService
from ..models.data_model import db,Course
from PIL import Image
from io import BytesIO
import base64

class CourseService:
    @staticmethod
    def get_all_courses():
        return Course.query.all()
    @staticmethod
    def get_course_by_id(courseId):
        return Course.query.get(courseId)
    @staticmethod
    def convert_image_to_base64(image_data):
        if image_data:
            base64_image = base64.b64encode(image_data).decode('utf-8')
            return base64_image
        return None
    @staticmethod
    def create_course(course_name, course_description, course_rate, course_path, provider_id, category_id, course_image):
        provider = ProviderService.get_provider_by_id(provider_id)
        category = CategoryService.get_category_by_id(category_id)

        if not provider or not category:
            raise ValueError("Invalid provider_id or category_id")

        # Convert image to binary data
        course_image_binary = None
        if course_image:
            image_stream = BytesIO(course_image.read())
            img = Image.open(image_stream)
            course_image_binary = image_stream.getvalue()

        new_course = Course(
            course_name=course_name,
            course_description=course_description,
            course_rate=course_rate,
            course_path=course_path,
            provider_id=provider_id,
            category_id=category_id,
            course_image=course_image_binary
        )

        db.session.add(new_course)
        db.session.commit()
        return new_course

    @staticmethod
    def edit_course(course_id, new_course_name, new_course_description, new_course_rate, new_course_path, new_provider_id, new_category_id, new_course_image):
        course = Course.query.get(course_id)
        if course:
            course.course_name = new_course_name
            course.course_description = new_course_description
            course.course_path = new_course_path
            course.course_rate = new_course_rate
            course.provider_id = new_provider_id
            course.category_id = new_category_id

            # Update image if provided
            if new_course_image:
                image_stream = BytesIO(new_course_image.read())
                img = Image.open(image_stream)
                course.course_image = image_stream.getvalue()

            db.session.commit()
            return course
        return None

    @staticmethod
    def delete_course(course_id):
        course = Course.query.get(course_id)
        if course:
            db.session.delete(course)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def search_course_by_name(input_name):
        courses = Course.query.filter(Course.course_name.ilike(f"%{input_name}%")).all()
        return courses
    
    @staticmethod
    def filter_courses(category=None, provider=None):
        query = Course.query
        if category:
            courses = query.filter_by(category_id = category).all()
        # if provider:
        #     query = query.filter_by(provider_id = provider)
        # courses = query.all()
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
        return courses_with_base64_images

