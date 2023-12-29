from flask_cors import CORS
from flask import Flask
from flask import redirect
from flask import url_for
from flask import request
from flask import abort

from dotenv import load_dotenv
import os

# Base de datos
from databases import ips

# Importamos las rutas
from security.routes import security_bp
from home.routes import home_bp 
from api.routes import api_bp
from chat.routes import chat_bp
from notify.routes import notify_bp
from configs.routes import configs_bp

# Inicializar base de datos
import init

# Cargamos las variables de entorno
load_dotenv()

# Verificamos los datos en la base de datos
base_datos = os.getenv('DB')
proyecto = os.getenv('NOMBRE')
init.initialize(base_datos, proyecto)

# Configuración Inicial
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_KEY')
CORS(app)

# Middleware
"""
@app.before_request
def restrict_by_ip():
    list_ips = ips.get_ips() + ['127.0.0.1']
    if request.remote_addr not in list_ips:
        abort(403) 
"""

# Ruta para enviar al Home cuando se ingresa al sitio
@app.route('/')
def index():
    return redirect(url_for('home.home'))

# Registramos las rutas
app.register_blueprint(security_bp)
app.register_blueprint(home_bp)
app.register_blueprint(api_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(notify_bp)
app.register_blueprint(configs_bp)

if __name__ == "__main__":
    debug = os.environ.get('DEBUG')
    app.run(
        debug=debug,
        host="0.0.0.0",
        port=5000
    )