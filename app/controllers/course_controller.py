from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from ..models.data_model import Course, CourseProgrammingLanguage,ProgrammingLanguage
from ..services.course_service import CourseService
from ..services.provider_service import ProviderService
from ..services.category_service import CategoryService
import pandas as pd
from PIL import Image
from io import BytesIO

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

def image_to_binary(image_path):
    print('cccc',image_path)
    try:
        # Đọc hình ảnh từ tệp
        image = Image.open(image_path)
        print('cccc',image)
        # Chuyển đổi hình ảnh thành dạng bytes
        image_bytes = BytesIO()
        image.save(image_bytes, format="JPG")  # Có thể chọn định dạng ảnh khác nếu cần
        return image_bytes.getvalue()
    except Exception as e:
        print(f"Error processing image: {e}")
        return None


@course_controller.route('/upload', methods=['POST'])
@login_required
def upload():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        df = pd.read_excel(file)
        # image_column_name = 'course_image'
        # Iterate over rows and read images
        # for idx, row in df.iterrows():
            # Assume the image column contains URLs
            # image_url = row[image_column_name]
            # print('course_image',image_url)
            # Download the image (you may need to use requests or another library)
            # image_content = download_image_content(image_url)

            # # Convert the image content to BytesIO
            # image_bytesio = BytesIO(image_content)

        
        # aaaa = image_to_binary(df['course_image'])
        # df['course_image'] = CourseService.convert_image_to_base64(df['course_image'])
        # CourseService.convert_image_to_base64(course.course_image),
        # df['course_image']=df['course_image'].apply(lambda image_path: image_to_binary(image_path))
        # print('a',aaaa)
        # for index, row in df.iterrows():
        #     course_image = row['course_image']
        #     image = Image.open(course_image)
        records = df.to_dict(orient='records')
        # for record in records:
        CourseService.insert_excel(records)
        #     new_doctor = Doctor(**record)
        #     db.session.add(new_doctor)

        # db.session.commit()

        return  redirect(url_for('main.course_controller.index'))



# Đọc dữ liệu từ file Excel
# wb = openpyxl.load_workbook('your_excel_file.xlsx')
# sheet = wb.active

# # Lặp qua từng dòng trong sheet
# for row in sheet.iter_rows(min_row=2, values_only=True):
#     name, age, image_data = row

#     # Chuyển đổi hình ảnh thành dạng byte
#     image = Image.open(BytesIO(image_data))
#     buffer = BytesIO()
#     image.save(buffer, format="PNG")  # Chọn định dạng ảnh theo nhu cầu của bạn
#     byte_image = buffer.getvalue()
#     buffer.close()

#     # Lưu trữ dạng byte_image vào cơ sở dữ liệu theo nhu cầu của bạn
#     # Ví dụ: In dạng base64 để lưu vào cơ sở dữ liệu
#     base64_image = base64.b64encode(byte_image).decode('utf-8')
#     print(f"Name: {name}, Age: {age}, Image in Base64: {base64_image}")

# wb.close()


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
