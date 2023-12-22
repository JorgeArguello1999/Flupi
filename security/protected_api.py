from functools import wraps
from flask import request, jsonify

from security.database import search_token

def token_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Obtener el token del JSON enviado a través del método POST
        token = request.json.get('token')

        # Verificar el token en la base de datos
        if not verificar_token(token):
            return jsonify({'message': 'Token inválido'}), 401

        # Si el token es válido, permite el acceso a la ruta
        return func(*args, **kwargs)

    return decorated_function

# Ejemplo de función que verifica el token en la base de datos (simulado)
def verificar_token(token):
    return search_token(token)
