from flask import Flask, jsonify, request
from flask import render_template
import markdown2

# Configuración inciial
app = Flask(__name__)

# Abrimos el README para mostrarlo en la Home
with open('README.md', 'r') as readme:
    readme = readme.read()

"""
/ -> Home
/chatbot/[GET] -> Pequeño chat interactivo con Maxi 
/chatbot/[POST] -> A traves del metodo post se envian las preguntas
/notify/[GET] -> Página para el técnico
"""

# Home
@app.route('/', methods=['GET'])
def home():
    mark_html = markdown2.markdown(readme)
    return render_template('index.html', markdown_text=mark_html)

@app.route('/chatbot/', methods=['GET'])
def chatbot_get():
    return render_template('chatbot.html')

if __name__ == "__main__":
    app.run(debug=True)
