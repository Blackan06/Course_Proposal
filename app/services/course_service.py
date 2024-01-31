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
            print(course_image)
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

        print(new_course)
        db.session.add(new_course)
        db.session.commit()
        return new_course
    
    @staticmethod
    def insert_excel(objects):   
        for obj in objects:
            provider = ProviderService.get_provider_by_id(obj.get('provider_id',0))
            category = CategoryService.get_category_by_id(obj.get('category_id',0))

            if not provider or not category:
                raise ValueError("Invalid provider_id or category_id")

            # Convert image to binary data
            course_image_binary = None
            if obj.get('course_image', 0.0):
                image_stream = BytesIO(obj.get('course_image', 0.0).read())
                course_image_binary = image_stream.getvalue()
                # course_image_float = obj.get('course_image', 0.0)

            # Convert float to bytes (binary)
            # course_image_data = str(course_image_float).encode('utf-8')
            new_course = Course(
                course_name=obj.get('course_name',''),
                course_description=obj.get('course_description',''),
                course_rate=obj.get('course_rate',0),
                course_path=obj.get('course_path',''),
                provider_id=provider,
                category_id=category,
                course_image=course_image_binary
            )
            try:
                db.session.add(new_course) 
                # return new_course
            except IntegrityError:
                db.session.rollback()
        db.session.commit()

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
