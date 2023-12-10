from flask import Flask, jsonify, request
from flask import render_template
from flask import redirect, url_for
from flask import send_from_directory
from flask_cors import CORS
from modules import voice, chatbot
import os


# Configuración inciial
app = Flask(__name__)
CORS(app)
app.config['STATIC_URL'] = '/static'

# Estado inicial del técnico
work = {'status': False}

# Acciones 
comandos = list(chatbot.actions.keys())

"""
=== HOME ===
Pagina principal
"""

# Home
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

"""
=== CHATBOT ===

El chatbot maneja las siguientes funciones:

- chatbot_get [GET]: Renderiza la página 'chatbot.html'.
- chatbot_post [POST]: Procesa la pregunta enviada al chatbot y responde según la pregunta.

"""

# Chatbot Front
@app.route('/chatbot/', methods=['GET'])
def chatbot_get():
    """
    Endpoint: /chatbot/ [GET]
    Descripción: Renderiza la plantilla 'chatbot.html'.
    Parámetros: Ninguno.
    Retorna: Página web para interactuar con el chatbot.
    """
    return render_template('chatbot.html', comandos=comandos)

# Chatbot Back
@app.route('/chatbot/', methods=['POST'])
def chatbot_post():
    """
    Endpoint: /chatbot/ [POST]
    Descripción: Procesa la pregunta enviada al chatbot y responde según la pregunta.
    Parámetros:
        - ask (str): Pregunta realizada al chatbot.
        - device (str): Dispositivo desde el cual se hace la consulta (opcional).
    Retorna: Respuesta del chatbot a la pregunta realizada.
    """
    data = request.get_json()
    pregunta = data["ask"]

    if pregunta.isdigit() == True:
        # Si la pregunta es un número, busca la descripción del producto
        respuesta = chatbot.get_product_description(pregunta)
    else:
        # Si no es un número, realiza una consulta al chatbot
        respuesta = chatbot.chatbot(pregunta)

    # Si la consulta es desde un dispositivo diferente a una computadora, devuelve un audio
    if data["device"] != "computer":
        salida = voice.speaker(respuesta)
        return send_from_directory('static/audio_chatbot', salida)

    return respuesta

"""
=== NOTIFY ===

El notify es donde se avisa al técnico que hay un usuario afuera. Se manejan los siguientes endpoints:

- notify_f [GET]: Renderiza la página web como tal para notificar.
- notify [GET]: Retorna el estado actual de la alarma.
- notify/int [GET]: Si se pasa '1' como parámetro, se activa la llamada al técnico.
"""

# Notify Front
@app.route('/notify_f', methods=['GET'])
def notify_frontend():
    """
    Endpoint: /notify_f [GET]
    Descripción: Renderiza la plantilla 'notify.html' para notificar al técnico.
    Parámetros: Ninguno.
    Retorna: Página web para notificar.
    """
    return render_template('notify.html')

# Notify Status
@app.route('/notify', methods=['GET'])
def notify_status():
    """
    Endpoint: /notify [GET]
    Descripción: Retorna el estado actual de la alarma.
    Parámetros: Ninguno.
    Retorna: JSON con el estado actual de la alarma.
    """
    return jsonify({
        "status": work["status"]
    })

# Notify Back
@app.route("/notify/<int:statuswork>", methods=["GET"])
def notify_backend(statuswork):
    """
    Endpoint: /notify/<int:statuswork> [GET]
    Descripción: Actualiza el estado de la alarma.
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