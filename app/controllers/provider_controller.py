from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from ..models.data_model import Provider
from ..services.provider_service import ProviderService
from flask_login import login_required
provider_controller = Blueprint('provider_controller', __name__, url_prefix='/provider')

@provider_controller.route('/', methods=['GET'])
@provider_controller.route('/index', methods=['GET'])
@login_required
def index():
    providers = ProviderService.get_all_provider()
    return render_template('providers/index.html', providers=providers)

@provider_controller.route('/create', methods=['GET','POST'])
@login_required
def create():
    try:
        if request.method == 'POST':
            provider_name = request.form['provider_name']
            ProviderService.create_provider(provider_name)
            return redirect(url_for('main.provider_controller.index'))
        else:
                return render_template('providers/create.html')

    except Exception as e:
        return jsonify(error=str(e)), 400

@provider_controller.route('/edit/<int:provider_id>', methods=['GET','POST'])
@login_required
def edit(provider_id):
    try:
        provider = Provider.query.get(provider_id)
        if request.method == 'POST':
            new_provider_name = request.form['provider_name']
            ProviderService.edit_provider(provider_id, new_provider_name)
            return redirect(url_for('main.provider_controller.index'))
        else:
            return render_template('providers/edit.html',provider=provider)

    except Exception as e:
        return jsonify(error=str(e)), 400

@provider_controller.route('/delete/<int:provider_id>', methods=['POST'])
@login_required
def delete(provider_id):
    try:
        success = ProviderService.delete_provider(provider_id)
       
    except Exception as e:
        return jsonify(error=str(e)), 400
