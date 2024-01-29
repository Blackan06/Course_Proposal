from ..models.data_model import CourseProgrammingLanguage
from ..models.db import db

class CourseProgrammingLanguageService:

    @staticmethod
    def get_all_course_programming_language():
        return CourseProgrammingLanguage.query.all()
    
    @staticmethod
    def get_course_programming_language_by_id(course_programming_language_id):
        return CourseProgrammingLanguage.query.get(course_programming_language_id)
    
    @staticmethod
    def create_course_programming_language(course_id, language_id):
        newCourseProgrammingLanguage = CourseProgrammingLanguage(course_id=course_id,language_id=language_id)
        db.session.add(newCourseProgrammingLanguage)
        db.session.commit()
        return newCourseProgrammingLanguage
    
    @staticmethod
    def edit_course_programming_language(course_programming_language_id,course_id,language_id):
        course_programming_language = CourseProgrammingLanguage.query.get(course_programming_language_id)
        if course_programming_language:
            course_programming_language.course_id = course_id
            course_programming_language.language_id = language_id
            db.session.commit()
            return course_programming_language
        return None
    @staticmethod
    def delete_course_programming_language(course_programming_language_id):
        course_programming_language = CourseProgrammingLanguage.query.get(course_programming_language_id)
        if course_programming_language:
            db.session.delete(course_programming_language)
            db.session.commit()
            return True
        return False
        
