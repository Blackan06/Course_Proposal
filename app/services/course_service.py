from ..services.category_service import CategoryService
from ..services.provider_service import ProviderService
from ..services.course_programming_language_service import CourseProgrammingLanguageService
from ..models.data_model import db,Course,CourseProgrammingLanguage,ProgrammingLanguage 

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
    def create_course(course_name, course_description, course_rate, course_path, provider_id, category_id,language_ids, course_image):
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
        
        languages = CourseProgrammingLanguage.query.filter(ProgrammingLanguage.language_id.in_(language_ids)).all()
        print('languages ', languages)
        for language in language_ids:
            new_course_programming_language = CourseProgrammingLanguage(
                course_id=new_course.course_id,
                language_id=language,
            )
            db.session.add(new_course_programming_language)

        db.session.commit()
        return new_course

    @staticmethod
    def edit_course(course_id, new_course_name, new_course_description, new_course_rate, new_course_path, new_provider_id, new_category_id,new_language_ids, new_course_image):
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
            
            current_languages = CourseProgrammingLanguage.query.filter_by(course_id=course.course_id).all()
            print('current_languages',current_languages)
            current_language_ids = set(language.language_id for language in current_languages)
            print('current_language_ids',current_language_ids)
            selected_language_ids_set = set(new_language_ids)
            print('selected_language_ids_set',selected_language_ids_set)

            new_languages_to_add = selected_language_ids_set - current_language_ids
            languages_to_remove = current_language_ids - selected_language_ids_set
            print('remove', languages_to_remove)

            for language_id in languages_to_remove:
                CourseProgrammingLanguage.query.filter_by(course_id=course.course_id, language_id=language_id).delete()
            
            print('add', new_languages_to_add)
            for language_id in new_languages_to_add:
                new_course_programming_language = CourseProgrammingLanguage(
                    course_id=course.course_id,
                    language_id=language_id
                )
                db.session.add(new_course_programming_language)
            
            


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
    def search_course_by_name(category, provider, programming_language, input_name=None):
        courses = Course.query
        if input_name:
            courses = courses.filter(Course.course_name.ilike(f"%{input_name}%"))
        if category != 'all':
            courses = courses.filter(Course.category_id == category)
        if provider != 'all':
            courses = courses.filter(Course.provider_id == provider)
        if programming_language != 'all':
            courses = (
            courses.join(CourseProgrammingLanguage)
            .filter(CourseProgrammingLanguage.language_id == programming_language)
        )
            
        courses = courses.all()
        return courses

    @staticmethod
    def filter_courses(category=None, provider=None):
        courses = Course.query
        if category != 'all':
            courses = courses.filter(Course.category_id == category)
        if provider != 'all':
            courses = courses.filter_by(provider_id = provider)
        courses = courses.all()
        return courses