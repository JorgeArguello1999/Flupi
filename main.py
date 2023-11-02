from flask import Flask, jsonify, request
from flask import render_template
from flask import redirect, url_for
from flask_cors import CORS
import markdown2

import sys

# Configuración inciial
app = Flask(__name__)
CORS(app)
app.config['STATIC_URL'] = '/static'

# Rutas del servidor
host = sys.argv[1]
port = sys.argv[2]

# Abrimos el README para mostrarlo en la Home
with open('README.md', 'r') as readme:
    readme = readme.read()

# Declaramos el estado inicial del trabajador
work = {'status': False}

"""
/ -> Home
/chatbot/[GET] -> Pequeño chat interactivo con Maxi 
/chatbot/[POST] -> A traves del metodo post se envian las preguntas
/notify/[GET] -> Página para el técnico

chatbot: Es como un pequeño sistema automatizado para realizar consultas
"""

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
    return data


# Notify Front
@app.route('/notify_f', methods=['GET'])
def notify_frontend():
    return render_template('notify.html', host=host, port=port)

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