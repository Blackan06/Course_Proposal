from flask import Blueprint, render_template, redirect, url_for , jsonify,request
from ..models.data_model import Skill
from ..services.skill_service import SkillService
from ..services.category_service import CategoryService
from flask_login import login_required
skill_controller = Blueprint('skill_controller', __name__, url_prefix='/skill')

@skill_controller.route('/', methods=['GET'])
@skill_controller.route('/index', methods=['GET'])
@login_required
def index():
    skills = SkillService.get_all_skill()
    return render_template('skills/index.html', skills=skills)

@skill_controller.route('/create', methods=['GET','POST'])
@login_required
def create():
    try:
        if request.method == 'POST':
            input_skill_name = request.form['skill_name']
            choose_category_id = request.form['category_id']
            SkillService.create_skill(input_skill_name,choose_category_id)
            return redirect(url_for('main.skill_controller.index'))
        else:
            categories = CategoryService.get_all_category()

            return render_template('skills/create.html',categories=categories)
 
    except Exception as e:
        return jsonify(error=str(e)), 400

@skill_controller.route('/edit/<int:skill_id>', methods=['GET','POST'])
@login_required
def edit(skill_id):
    try:
        if request.method == 'POST':
        
            skill = Skill.query.get(skill_id)
            new_skill_name = request.form['skill_name']
            new_category_id = request.form['new_category_id']
            SkillService.edit_skill(skill_id, new_skill_name,new_category_id)
            return redirect(url_for('main.skill_controller.index'))
        else:
            categories = CategoryService.get_all_category()

            return render_template('skills/edit.html',categories=categories)

    except Exception as e:
        return jsonify(error=str(e)), 400

@skill_controller.route('/delete/<int:skill_id>', methods=['DELETE'])
@login_required
def delete(skill_id):
    try:
        success = SkillService.delete_skill(skill_id)
        if success:
            return redirect(url_for('main.skill_controller.index'))
    except Exception as e:
        return jsonify(error=str(e)), 400
