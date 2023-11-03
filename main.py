from flask import Flask, jsonify, request
from flask import render_template
from flask import redirect, url_for
from flask_cors import CORS

import markdown2
import chatbot
import sys

# Configuración inciial
app = Flask(__name__)
CORS(app)
app.config['STATIC_URL'] = '/static'

# Abrimos el README para mostrarlo en la Home
with open('README.md', 'r') as readme:
    readme = readme.read()

# Declaramos el estado inicial del trabajador
work = {'status': False}

# Home
@app.route('/', methods=['GET'])
def home():
    mark_html = markdown2.markdown(readme)
    return render_template('index.html', markdown_text=mark_html)


# Chatbot Front
@app.route('/chatbot/', methods=['GET'])
def chatbot_get():
    return render_template('chatbot.html')

# Chatbot Back
@app.route('/chatbot/', methods=['POST'])
def chatbot_post():
    data = request.get_json()

    # Respondiendo la pregunta
    pregunta = data["ask"]
    respuesta = chatbot.chatbot(pregunta)

    # En caso de ser para el bot, enviamos un Audio
    if data["device"] == "bot":
        return 0
    
    return respuesta 


# Notify Front
@app.route('/notify_f', methods=['GET'])
def notify_frontend():
    return render_template('notify.html', host='127.0.0.1', port=5000)

# Notify Status
@app.route('/notify', methods=['GET'])
def notify_status():
    return jsonify({
        "status": work["status"]
    })

# Notify Back
@app.route("/notify/<int:statuswork>", methods=["GET"])
def notify_backend(statuswork):
    status = False
    if statuswork == 1:
        status = True
    work["status"] = status

    return redirect(url_for('notify_frontend'))

if __name__ == "__main__":
    app.run(debug=True)