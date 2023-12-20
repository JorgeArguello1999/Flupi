from flask import Blueprint, render_template
from flask import request 
from flask import session
from flask import redirect
from flask import url_for

from security import database

security_bp = Blueprint('security', __name__, url_prefix='/security', template_folder='templates', static_folder='static')

# Login
@security_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        salida = database.search_user(username, password)
        print(salida)
        if database.search_user(username, password):
            session['username'] = username
            return redirect(url_for('home.home'))

        else:
            error = "Credenciales invalidas"
            return render_template('login.html', error=error)

    return render_template('login.html')

@security_bp.route('logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for('security.login'))