from flask import Blueprint, render_template
from flask import request

import json

from api import logic

from security.protected_routes import requerir_autenticacion
from security.protected_api import token_required

api_bp = Blueprint('api', __name__, url_prefix='/api', static_folder='static', template_folder='templates')

# API para el chatbot
@api_bp.route("/", methods=['GET'])
@requerir_autenticacion
def api_get():
    with open('./api/static/info.json', 'r') as file:
        json_data = json.load(file)
    return render_template('api_information.html', json=json_data)

@api_bp.route("/", methods=['POST'])
@token_required
def api_post():
    data = request.get_json()

    print(f'User: <<{data["user"]}>> Token: <<{data["token"]}>>')

    if str(data['device']).lower() == 'bot':
        return logic.bot(data)
    
    if data['ask'].isdigit():
        return logic.productos(data)
    
    return logic.computer(data)