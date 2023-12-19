from flask import Flask, jsonify, request
from flask import render_template
from flask import redirect, url_for
from flask import send_from_directory
from flask_cors import CORS

import os
import datetime
import sqlite3

import _database_

# Configuración inciial
app = Flask(__name__)
CORS(app)
app.config['STATIC_URL'] = '/static'

# Acciones 
comandos = list(chatbot.actions.keys())

# Chatbot Front
@app.route('/chatbot/', methods=['GET'])
def chatbot_get():
    return render_template('chatbot.html', comandos=comandos)


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
    content = context.get_context(filename)

    return jsonify({
        'filename': filename, 
        'content': content
    })

@app.route('/context/<filename>', methods=['POST'])
def update_context(filename):
    content = request.json.get('content')
    content = context.update_context(filename, content)
    if content:
        salida = 'File updated successfully'
    else:
        salida = 'Error'

    return jsonify({
        'filename': filename, 
        'message': salida
    })

@app.route('/context_f/', methods=['GET'])
def read_context():
    context_files = context.get_context_all()
    return render_template('context.html', files=context_files)

# Ruta para obtener una imagen por su nombre
@app.route('/images/<filename>', methods=['GET'])
def get_image(filename):
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()

    cursor.execute("SELECT image FROM Fotos WHERE name=?", (filename,))
    image_data = cursor.fetchone()

    conn.close()

    if image_data:
        return jsonify({'filename': filename, 'content': image_data[0]})
    else:
        return jsonify({'message': 'Image not found'})

# Ruta para actualizar una imagen
@app.route('/images/<filename>', methods=['POST'])
def update_image(filename):
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()

    new_image = request.files['new_image']
    new_image_data = new_image.read()

    # Actualizar la imagen en la base de datos
    cursor.execute("UPDATE Fotos SET image=? WHERE name=?", (new_image_data, filename))
    conn.commit()
    conn.close()

    return jsonify({'filename': filename, 'message': 'File updated successfully'})

# Ruta para obtener la lista de imágenes
@app.route('/images_f/', methods=['GET'])
def read_images():
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM Fotos")
    image_names = [row[0] for row in cursor.fetchall()]

    conn.close()

    return render_template('change_images.html', files=image_names)

if __name__ == "__main__":
    app.run(
        debug=os.environ.get("DEBUG"),
        host="0.0.0.0",
        port=5000
    )