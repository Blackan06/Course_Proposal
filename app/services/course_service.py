
from ..models.data_model import Course
from ..models.db import db

class CourseService:
    @staticmethod
    def get_all_courses():
        return Course.query.all()

    @staticmethod
    def create_course(course_name,):
        new_course = Course(course_name=course_name)
        db.session.add(new_course)
        db.session.commit()
        return new_course

    @staticmethod
    def edit_course(course_id, new_course_name):
        course = Course.query.get(course_id)
        if course:
            course.course_name = new_course_name
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
