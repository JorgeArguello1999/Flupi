from flask import Flask, jsonify, request
from flask import render_template
from flask import redirect, url_for
from flask import send_from_directory
from flask_cors import CORS

import os
import datetime

from modules import voice 
from modules import chatbot
from modules import chatgpt
from modules import context
import _database_

# Configuración inciial
app = Flask(__name__)
CORS(app)
app.config['STATIC_URL'] = '/static'

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

# API para el chatbot
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
    work = _database_.get_alarm_status()

    return jsonify({
        "status": work
    })

# Notify Back
@app.route("/notify/<int:statuswork>", methods=["GET"])
def notify_backend(statuswork):
    """
    Parámetros:
        - statuswork (int): 1 para llamar al técnico, 0 para desactivar.
    Retorna: Redirección a la página 'notify_f'.
    """
    _database_.update_alarm_status(statuswork)
    return redirect(url_for('notify_frontend'))

# Ruta para modificar el contexto
@app.route('/context/<filename>', methods=['GET'])
def get_context(filename):
    with open(f'context/{filename}', 'r') as file:
        content = file.read()
    return jsonify({'filename': filename, 'content': content})

@app.route('/context/<filename>', methods=['POST'])
def update_context(filename):
    content = request.json.get('content')
    with open(f'context/{filename}', 'w') as file:
        file.write(content)
    return jsonify({'filename': filename, 'message': 'File updated successfully'})

@app.route('/context_f/', methods=['GET'])
def read_context():
    context_files = os.listdir('context') 
    return render_template('context.html', files=context_files)

# Ruta para las imagenes
@app.route('/images/<filename>', methods=['GET'])
def get_image(filename):
    with open(f'uploads/{filename}', 'rb') as file:
        content = file.read()
    return jsonify({'filename': filename, 'content': content})

@app.route('/images/<filename>', methods=['POST'])
def update_image(filename):
    new_image = request.files['new_image']
    new_image.save(os.path.join('uploads', filename))
    return jsonify({'filename': filename, 'message': 'File updated successfully'})

@app.route('/images_f/', methods=['GET'])
def read_images():
    images_files = os.listdir('uploads') 
    return render_template('change_images.html', files=images_files)


if __name__ == "__main__":
    app.run(
        debug=os.environ.get("DEBUG"),
        host="0.0.0.0",
        port=5000
    )