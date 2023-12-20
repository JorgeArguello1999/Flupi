from flask import session, redirect, url_for
from functools import wraps

# Función para verificar si el usuario está autenticado
def verificar_autenticacion():
    return 'username' in session

# Decorador para verificar la autenticación antes de acceder a una ruta
def requerir_autenticacion(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if not verificar_autenticacion():
            return redirect(url_for('security.login'))
        return route_function(*args, **kwargs)
    return wrapper