from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from ..models.data_model import ProgrammingLanguage
from ..services.programming_language_service import ProgrammingLanguageService
from flask_login import login_required
programming_language_controller = Blueprint('programming_language_controller', __name__, url_prefix='/programminglanguage')

@programming_language_controller.route('/', methods=['GET'])
@programming_language_controller.route('/index', methods=['GET'])
@login_required
def index():
    programming_languages = ProgrammingLanguageService.get_all_programming_language()
    return render_template('programming_languages/index.html', programming_languages=programming_languages)

@programming_language_controller.route('/create', methods=['GET','POST'])
@login_required
def create():
    try:
        if request.method == 'POST':
            language_name = request.form['language_name']
            ProgrammingLanguageService.create_programming_language(language_name)
            return redirect(url_for('main.programming_language_controller.index'))
        else:
            return render_template('programming_languages/create.html')

    except Exception as e:
        return jsonify(error=str(e)), 400

@programming_language_controller.route('/edit/<int:language_id>', methods=['GET','POST'])
@login_required
def edit(language_id):
    try:
        programming_language = ProgrammingLanguage.query.get(language_id)
        if request.method == 'POST':

            new_language_name = request.form['language_name']
            ProgrammingLanguageService.edit_programming_language(language_id, new_language_name)
            return redirect(url_for('main.programming_language_controller.index'))
        else:
            return render_template('programming_languages/edit.html',programming_language=programming_language)

    except Exception as e:
        return jsonify(error=str(e)), 400

@programming_language_controller.route('/delete/<int:language_id>', methods=['POST'])
@login_required
def delete(language_id):
    try:
        success = ProgrammingLanguageService.delete_programming_language(language_id)
       
    except Exception as e:
        return jsonify(error=str(e)), 400
