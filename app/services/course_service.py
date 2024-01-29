from ..services.category_service import CategoryService
from ..services.provider_service import ProviderService
from ..models.data_model import Course
from ..models.db import db

class CourseService:
    @staticmethod
    def get_all_courses():
        return Course.query.all()
    @staticmethod
    def get_course_by_id(courseId):
        return Course.query.get(courseId)

    @staticmethod
    def create_course(course_name,course_description,course_rate,course_path,provider_id,category_id):
        provider = ProviderService.get_provider_by_id(provider_id)
        category = CategoryService.get_category_by_id(category_id)

        if not provider or not category:
            raise ValueError("Invalid provider_id or category_id")
        new_course = Course(course_name=course_name,course_description=course_description,course_rate=course_rate,course_path=course_path,provider_id=provider_id,category_id=category_id)
        db.session.add(new_course)
        db.session.commit()
        return new_course

    @staticmethod
    def edit_course(course_id, new_course_name,new_course_description,new_course_rate, new_course_path, new_provider_id, new_category_id):
        course = Course.query.get(course_id)
        if course:
            course.course_name = new_course_name
            course.course_description = new_course_description
            course.course_path = new_course_path
            course.course_rate = new_course_rate
            course.provider_id = new_provider_id
            course.category_id = new_category_id
            
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
