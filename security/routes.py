from flask import Blueprint 
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for

from databases import usuarios
from security.protected_routes import requerir_autenticacion

from dotenv import load_dotenv
load_dotenv()

import os

security_bp = Blueprint('security', __name__, url_prefix='/security', template_folder='templates', static_folder='static')

@security_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = usuarios.get_user_by_username(username)
        if user and usuarios.search_user(username, password):
            session['username'] = username
            return redirect(url_for('home.home'))
        else:
            error = "Credenciales inválidas"
            return render_template('login.html', error=error)

    return render_template('login.html')

@security_bp.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for('security.login'))


# Esta ruta es solo accesible si se tiene acceso al sistema
@security_bp.route('/signup', methods=['GET', 'POST'])
@requerir_autenticacion
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if usuarios.get_user_by_username(username):
            error = "El nombre de usuario ya está en uso. Por favor, elige otro."
            return render_template('signup.html', error=error)

        usuarios.create_user(username, password)
        return redirect(url_for('security.login'))

    return render_template('signup.html')

# Gestion de usuarios
@security_bp.route('/users')
@requerir_autenticacion
def view_users():
    users = usuarios.get_all_users()
    return render_template('view_users.html', users=users)

@security_bp.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
@requerir_autenticacion
def delete_user(user_id):
    if request.method == 'POST':
        password = request.form['password']

        if password == os.environ.get('ADMIN_KEY'):
            usuarios.delete_user_by_id(user_id)
            return redirect(url_for('security.view_users'))
        else:
            error = "Contraseña incorrecta para eliminar usuario."
            return render_template('delete_user.html', error=error)

    return render_template('delete_user.html')