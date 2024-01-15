from flask import Blueprint, render_template
from flask import request
from flask import jsonify
from flask import url_for

from databases import usuarios

import requests

chat_bp = Blueprint('chatbot', __name__, url_prefix='/chatbot', template_folder='templates', static_folder='static')

# Chatbot Front
@chat_bp.route('/', methods=['GET'])
def chatbot_get():
    try:
        chatbot = usuarios.get_user_by_username('chatbot')[1]
    except:
        chatbot = "No existe usuario"
    return render_template('chatbot.html', token=chatbot)


# Chatbot Back
@chat_bp.route('/', methods=['POST'])
def chatbot_post():
    data = request.get_json()
    token = usuarios.get_user_by_username('chatbot')[1]

    data = {
        "user": "Chatbot",
        "device": "computer",
        "ask": data['ask'],
        "token": token
    }

    try:
        response = requests.post('http://127.0.0.1:5000/api', json=data)
        return jsonify(response.json())
    
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({"error": str(e)})
