from flask import Blueprint, render_template
from flask import request
from flask import jsonify

from databases import database
from databases import contextos

from security.protected_routes import requerir_autenticacion

configs_bp = Blueprint('configs', __name__, url_prefix='/configs', template_folder='templates', static_folder='static')

# Ruta para modificar el contexto
@configs_bp.route('/context/<filename>', methods=['GET'])
@requerir_autenticacion
def get_context(filename):
    content = contextos.get_context(filename)

    return jsonify({
        'filename': filename, 
        'content': content
    })

@configs_bp.route('/context/<filename>', methods=['POST'])
@requerir_autenticacion
def update_context(filename):
    content = request.json.get('content')
    content = database.update_context(filename, content)
    if content:
        salida = 'File updated successfully'
    else:
        salida = 'Error'

    return jsonify({
        'filename': filename, 
        'message': salida
    })

@configs_bp.route('/context_f/', methods=['GET'])
@requerir_autenticacion
def read_context():
    context_files = contextos.get_context_all()
    return render_template('context.html', files=context_files)


# Rutas para las imagenes
@configs_bp.route('/images/<filename>', methods=['GET'])
@requerir_autenticacion
def get_image_route(filename):
    image_data = database.get_image(filename)

    if image_data != 'Image not found':
        return jsonify({'filename': filename, 'content': image_data})
    else:
        return jsonify({'message': 'Image not found'})

@configs_bp.route('/images/<filename>', methods=['POST'])
@requerir_autenticacion
def update_image_route(filename):
    new_image = request.files['new_image']
    new_image_data = new_image.read()

    result = database.update_image(filename, new_image_data)

    if result == "Imagen actualizada correctamente en la base de datos.":
        return jsonify({'filename': filename, 'message': 'File updated successfully'})
    else:
        return jsonify({'filename': filename, 'message': result})

@configs_bp.route('/images_f/', methods=['GET'])
@requerir_autenticacion
def read_images_route():
    image_names = database.get_image_all()
    return render_template('change_images.html', files=image_names)