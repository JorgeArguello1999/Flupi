from flask import Blueprint, render_template
from flask import request
from flask import jsonify

import base64

from configs import context
from configs import images

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


# Rutas para las imagenes
@configs_bp.route('/images/<filename>', methods=['GET'])
def get_image_route(filename):
    image_data = images.get_image(filename)

    if image_data != 'Image not found':
        # Codificar la imagen en base64
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        return jsonify({'filename': filename, 'content': encoded_image})
    else:
        return jsonify({'message': 'Image not found'})

@configs_bp.route('/images/<filename>', methods=['POST'])
def update_image_route(filename):
    new_image = request.files['new_image']
    new_image_data = new_image.read()

    result = images.update_image(filename, new_image_data)

    if result == "Imagen actualizada correctamente en la base de datos.":
        return jsonify({'filename': filename, 'message': 'File updated successfully'})
    else:
        return jsonify({'filename': filename, 'message': result})

@configs_bp.route('/images_f/', methods=['GET'])
def read_images_route():
    image_names = images.get_image_all()
    return render_template('change_images.html', files=image_names)