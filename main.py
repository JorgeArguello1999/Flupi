from flask import Flask, jsonify, request
from flask import render_template
from flask import redirect, url_for
from flask import send_from_directory
from flask_cors import CORS
from modules import voice, chatbot

import os
import datetime

from modules import chatgpt
from modules import context


# Configuración inciial
app = Flask(__name__)
CORS(app)
app.config['STATIC_URL'] = '/static'

# Estado inicial del técnico
work = {'status': False}

# Acciones 
comandos = list(chatbot.actions.keys())

# Home
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


# Chatbot Front
@app.route('/chatbot/', methods=['GET'])
def chatbot_get():
    return render_template('chatbot.html', comandos=comandos)

# API
@app.route("/api/", methods=['GET'])
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
                "time_request": "00:01"
            }
        }
   })

@app.route("/api/", methods=['POST'])
def api_post():
    # Obtenemos la hora de Petición
    hora_peticion =  datetime.datetime.now().strftime('%H:%M')
    # Obtenemos el JSON
    data = request.get_json()

    # Enviamos a ChatGPT para que nos devuelva que pide el usuario
    response = chatgpt.answer(
        user= data["user"],
        ask= data["ask"],
        context= f"{context.entender_consulta} tu eres: {context.context}"
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

    # Salida de la API
    response = {
        "user": data["user"],
        "ask": data["ask"],
        "role": "assitant", 
        "response": response,
        "time_request": hora_peticion,
        "time_answer": hora_respuesta
    }

    return jsonify(response)


# Notify Front
@app.route('/notify_f', methods=['GET'])
def notify_frontend():
    return render_template('notify.html')

# Notify Status
@app.route('/notify', methods=['GET'])
def notify_status():
   return jsonify({
        "status": work["status"]
    })

# Notify Back
@app.route("/notify/<int:statuswork>", methods=["GET"])
def notify_backend(statuswork):
    """
    Parámetros:
        - statuswork (int): 1 para llamar al técnico, 0 para desactivar.
    Retorna: Redirección a la página 'notify_f'.
    """
    status = False
    if statuswork == 1:
        status = True
    work["status"] = status

    return redirect(url_for('notify_frontend'))


if __name__ == "__main__":
    app.run(
        debug=os.environ.get("DEBUG"),
        host="0.0.0.0",
        port=5000
    )