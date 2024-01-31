from flask import Blueprint, render_template, redirect, url_for , jsonify,request
from ..models.data_model import Skill
from ..services.skill_service import SkillService
from ..services.category_service import CategoryService
from flask_login import login_required
skill_controller = Blueprint('skill_controller', __name__, url_prefix='/skill')

@skill_controller.route('/index/<int:category_id>', methods=['GET'])
@login_required
def index(category_id):
    category = CategoryService.get_category_by_id(category_id)
    if category:
        skills = SkillService.get_all_skill(category_id)
        return render_template('skills/index.html', skills=skills, category=category)
    

@skill_controller.route('/create/<int:category_id>', methods=['GET','POST'])
@login_required
def create(category_id):
    try:
        category = CategoryService.get_category_by_id(category_id)

        if request.method == 'POST':
            input_skill_name = request.form['skill_name']
            SkillService.create_skill(input_skill_name,category_id)
            return redirect(url_for('main.skill_controller.index',category_id=category_id))
        else:

            return render_template('skills/create.html',category=category)
 
    except Exception as e:
        return jsonify(error=str(e)), 400

@skill_controller.route('/edit/<int:skill_id>', methods=['GET','POST'])
@login_required
def edit(skill_id):
    try:
        skill = Skill.query.get(skill_id)

        if request.method == 'POST':
        
            skill_name = request.form['skill_name']
            SkillService.edit_skill(skill_id, skill_name,skill.category_id)
            return redirect(url_for('main.skill_controller.index', category_id=skill.category_id))
        else:

            return render_template('skills/edit.html',skill=skill)

    except Exception as e:
        return jsonify(error=str(e)), 400

@skill_controller.route('/delete/<int:skill_id>/<int:category_id>', methods=['POST'])
@login_required
def delete(skill_id,category_id):
    try:
        
        success = SkillService.delete_skill(skill_id)
        category = CategoryService.get_category_by_id(category_id)
        if category:
            skills = SkillService.get_all_skill(category_id)
            return render_template('skills/index.html', skills=skills, category=category)
    except Exception as e:
        return jsonify(error=str(e)), 400
