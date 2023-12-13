from flask import Flask, jsonify, request
from flask import render_template
from flask import redirect, url_for
from flask import send_from_directory
from flask_cors import CORS
from modules import voice, chatbot
import os
import requests

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

# Chatbot Back
"""
@app.route('/chatbot/', methods=['POST'])
def chatbot_post():
    Parámetros:
        - ask (str): Pregunta realizada al chatbot.
        - device (str): Dispositivo desde el cual se hace la consulta (opcional).
    Retorna: Respuesta del chatbot a la pregunta realizada.
    data = request.get_json()

    data = {
        "ask" : data["ask"],
        "user" : "Bot",
        "device": data["device"]
    }

    if data["ask"].isdigit() == True:
        # Si la pregunta es un número, busca la descripción del producto
        respuesta = chatbot.get_product_description(data["ask"])
    else:
        # Si no es un número, realiza una consulta al chatbot
        respuesta = requests.post(url=url_for('api_post'), data=data)

    # Si la consulta es desde un dispositivo diferente a una computadora, devuelve un audio
    if data["device"] != "computer":
        salida = voice.speaker(respuesta)
        return send_from_directory('static/audio_chatbot', salida)

    return respuesta
"""
@app.route("/chatbot", methods=['POST'])
def chatbot_post():
    data = request.get_json()

    data = {
        "user": data["user"],
        "ask": data["ask"],
        "device": data["device"]
    }

    response = requests.post(
        url= url_for('api_post'),
        json= data
    )
    return response 

# API
@app.route("/api", methods=['GET'])
def api_get():
    return jsonify({
        "manual": "En el <body_form> muestro como se debe consultar",
        "method": {
            "GET": "Esta página",
            "POST": "Interacción con la API"
        },
        "formato": "JSON",
        "body_form": {
            "user": "Nombre del Usuario",
            "ask": "Pregunta del usuario",
            "device": "Computer o Bot"
        },
        "ejemplo": {
            "user": "Jorge",
            "ask": "Tienes teclados?",
            "device": "Computer"
        },
        "Devueleve": {
            "user": "Jorge",
            "ask": "Tienes teclados?",
            "role": "assistant",
            "response": "Datos",
        }
   })

@app.route("/api", methods=['POST'])
def api_post():
    # Obtenemos el JSON
    data = request.get_json()

    user = {
        "user": data["user"],
        "ask": data["ask"],
        "device": data["device"]
    }

    # Cargamos el contexto para identificar que necesita el usuario
    contexto = context.entender_consulta

    # Enviamos a ChatGPT para que nos devuelva que pide el usuario
    response = chatgpt.answer(
        user= user["user"],
        ask= user["ask"],
        context= contexto
    )

    response = chatbot.chatbot(response["response"])

    # Salida de la API
    response = {
        "user": user["user"],
        "ask": user["ask"],
        "role": "assitant", 
        "response": response["response"]
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