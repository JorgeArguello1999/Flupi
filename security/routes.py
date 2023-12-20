from flask import Blueprint 
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for

from security import database

security_bp = Blueprint('security', __name__, url_prefix='/security', template_folder='templates', static_folder='static')

@security_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = database.get_user_by_username(username)
        if user and database.search_user(username, password):
            session['username'] = username
            return redirect(url_for('home.home'))
        else:
            error = "Credenciales inválidas"
            return render_template('login.html', error=error)

    return render_template('login.html')

@security_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if database.get_user_by_username(username):
            error = "El nombre de usuario ya está en uso. Por favor, elige otro."
            return render_template('signup.html', error=error)

        database.create_user(username, password)
        return redirect(url_for('security.login'))

    return render_template('signup.html')

@security_bp.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for('security.login'))