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
from configs import voice


from databases import contextos

from databases.usuarios import get_user_by_username
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
                "time_request": "00:01"
            },
            "photos": {
                "adicional": {
                    "Fotos de usuario": "Las fotos de usuario se han movido a la ruta",
                    "ruta": "widget/photos/"
                },
                "Fotos Estructura": {
                    "GET": {
                        "photo_user": "foto_base64",
                        "photo_role": "foto_base64"
                    }
                }
            }
        }
    })
    return render_template('api_information.html', json=json)

@api_bp.route("/", methods=['POST'])
@token_required
def api_post():
    def get_current_time():
        return datetime.datetime.now().strftime('%H:%M')

    # Obtenemos la hora de Petición
    hora_peticion = get_current_time()
    
    # Obtenemos el JSON
    data = request.get_json()

    if data['ask'].isdigit():
        # En caso de que envíe solo dígitos
        response = api_compumax.search_product(data['ask'])
    else:
        # Enviamos a ChatGPT para que nos devuelva lo que pide el usuario
        chat_response = chatgpt.answer(
            user=data["user"],
            ask=data["ask"],
            context=f"{contextos.get_context('entender_consulta')} tu eres: {contextos.get_context('general')}"
        )

        comandos = chatbot.chatbot(chat_response["response"])

        # Se comprueba si se activó algún comando
        response = comandos["response"] if comandos else chat_response["response"]

        if data["device"] == "bot":
            response = voice.speaker(response)
            return send_from_directory('./audios', response)

    # Obtenemos hora respuesta
    hora_respuesta = get_current_time()

    # Salida de la API
    api_response = {
        "user": data["user"],
        "ask": data["ask"],
        "role": "assistant",
        "response": response,
        "time_request": hora_peticion,
        "time_answer": hora_respuesta
    }

    print(f'API Usuario: <<{data["user"]}>> Token: <<{data["token"]}>>')

    print(f"<<Pregunta>>: {api_response['ask']} <<Respuesta>>: {api_response['response']}")

    return jsonify(api_response)