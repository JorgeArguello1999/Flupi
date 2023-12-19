from flask import Blueprint, render_template
from flask import request
from flask import jsonify

import sqlite3

configs_bp = Blueprint('configs_bp', __name__, url_prefix='/configs', template_folder='templates', static_folder='static')

# Ruta para modificar el contexto
@configs_bp.route('/context/<filename>', methods=['GET'])
def get_context(filename):
    content = context.get_context(filename)

    return jsonify({
        'filename': filename, 
        'content': content
    })

@configs_bp.route('/context/<filename>', methods=['POST'])
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

@configs_bp.route('/context_f/', methods=['GET'])
def read_context():
    context_files = context.get_context_all()
    return render_template('context.html', files=context_files)

# Ruta para obtener una imagen por su nombre
@configs_bp.route('/images/<filename>', methods=['GET'])
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
@configs_bp.route('/images/<filename>', methods=['POST'])
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
@configs_bp.route('/images_f/', methods=['GET'])
def read_images():
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM Fotos")
    image_names = [row[0] for row in cursor.fetchall()]

    conn.close()

    return render_template('change_images.html', files=image_names)