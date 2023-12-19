from flask import Blueprint, render_template
from flask import jsonify
from flask import send_from_directory
from flask import request

import datetime

from configs import chatgpt
from configs import chatbot
from configs import context
from configs import voice
from configs import images

api_bp = Blueprint('api', __name__, url_prefix='/api')

# API para el chatbot
@api_bp.route("/", methods=['GET'])
def api_get():
    return jsonify({
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
                "device": "Computer"
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

@api_bp.route("/", methods=['POST'])
def api_post():
    # Obtenemos la hora de Petición
    hora_peticion =  datetime.datetime.now().strftime('%H:%M')
    # Obtenemos el JSON
    data = request.get_json()

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
        return send_from_directory('static/audio_chatbot', response)

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