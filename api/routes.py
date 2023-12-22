from flask import Blueprint, render_template
from flask import jsonify
from flask import send_from_directory
from flask import request
from flask import url_for

import datetime
import requests
import json

from configs import api_compumax
from configs import chatgpt
from configs import chatbot
from configs import context
from configs import voice
from configs import images

from security.database import get_user_by_username

from security.protected_routes import requerir_autenticacion
from security.protected_api import token_required

api_bp = Blueprint('api', __name__, url_prefix='/api', static_folder='static', template_folder='templates')

# API para el chatbot
@api_bp.route("/", methods=['GET'])
@requerir_autenticacion
def api_get():
    json = ({
        "formato": "JSON",
        "method": {
            "GET": "Esta página",
            "POST": "Interacción con la API"
        },
        "body_form": {
            "user": "Nombre del Usuario",
            "ask": "Pregunta del usuario",
            "device": "Computer o Bot"
        },
        "ejemplo": {
            "request_json": {
                "user": "Jorge",
                "ask": "Tienes teclados?",
                "device": "Computer",
                "token": "Tu token"
            },
            "response_json": {
                "user": "Jorge",
                "ask": "Tienes teclados?",
                "role": "assistant",
                "response": "Datos",
                "time_answer": "00:01",
                "time_request": "00:01",
                "photo_role": "fotografia_base64",
                "photo_user": "fotografia_base64"
            }
        }
    })
    return render_template('api_information.html', json=json)

@api_bp.route("/chat", methods=['POST'])
def api_middleware():
    data = request.get_json()
    token = get_user_by_username('chatbot')[3]

    data = {
        "user": data["user"],
        "ask": data["ask"],
        "device": data["device"],
        "token": token
    }

    # Convertir el diccionario 'data' a formato JSON
    json_data = json.dumps(data)

    salida = requests.post(
        url='http://127.0.0.1:5000/api/',
        data=json_data,  # Enviar el JSON en lugar de un diccionario Python
        headers={"Content-Type": "application/json"}
    ).json()

    return jsonify(salida)


@api_bp.route("/", methods=['POST'])
@token_required
def api_post():
    # Obtenemos la hora de Petición
    hora_peticion =  datetime.datetime.now().strftime('%H:%M')
    # Obtenemos el JSON
    data = request.get_json()

    # En caso de que envie solo digitos
    if data['ask'].isdigit():
        response = api_compumax.search_product(data['ask']) 

    else:
        # Enviamos a ChatGPT para que nos devuelva que pide el usuario
        response = chatgpt.answer(
            user= data["user"],
            ask= data["ask"],
            context= f"{context.get_context('entender_consulta')} tu eres: {context.get_context('context')}"
        )

        comandos = chatbot.chatbot(response["response"])

        # Se comprueba si se activo algún comando
        if comandos:
            response = comandos["response"]
        
        # Caso contrario se devuelve la respuesta de GPT 
        else:
            response = response["response"]

        if data["device"] == "bot":
            response = voice.speaker(response)
            return send_from_directory('./audios', response)

    # Obtenemos hora respuesta
    hora_respuesta =  datetime.datetime.now().strftime('%H:%M')

    photo_chatbot = images.get_image('chatbot')
    photo_user = images.get_image('usuario')

    # Salida de la API
    response = {
        "user": data["user"],
        "ask": data["ask"],
        "role": "assistant", 
        "response": response,
        "time_request": hora_peticion,
        "time_answer": hora_respuesta,
        "photo_user": photo_user,
        "photo_role": photo_chatbot
    }

    return jsonify(response)