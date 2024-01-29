from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from ..models.data_model import Category
from ..services.category_service import CategoryService
from flask_login import login_required
category_controller = Blueprint('category_controller', __name__, url_prefix='/category')

@category_controller.route('/', methods=['GET'])
@category_controller.route('/index', methods=['GET'])
@login_required
def index():
    categories = CategoryService.get_all_category()
    return render_template('categories/index.html', categories=categories)

@category_controller.route('/create', methods=['GET','POST'])
@login_required
def create():
    try:
        if request.method == 'POST':
            category_name = request.form['category_name']
            CategoryService.create_category(category_name)
            return redirect(url_for('main.category_controller.index'))
        else:
            return render_template('categories/create.html')
    except Exception as e:
        return jsonify(error=str(e)), 400

@category_controller.route('/edit/<int:category_id>', methods=['GET','POST'])
@login_required
def edit(category_id):
    try:
        if request.method == 'POST':
            category = CategoryService.get_category_by_id(category_id)
            new_category_name = request.form['category_name']
            CategoryService.edit_category(category_id, new_category_name)
            return redirect(url_for('main.category_controller.index'))
        else:
            return render_template('categories/edit.html')
    except Exception as e:
        return jsonify(error=str(e)), 400

@category_controller.route('/delete/<int:category_id>', methods=['DELETE'])
@login_required
def delete(category_id):
    try:
        success = CategoryService.delete_category(category_id)
        if success:
            return redirect(url_for('main.category_controller.index'))
    except Exception as e:
        return jsonify(error=str(e)), 400
