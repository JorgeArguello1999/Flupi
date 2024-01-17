from flask_cors import CORS
from flask import Flask, redirect, url_for, request, abort

from dotenv import load_dotenv
import os

# Base de datos
from databases import ips
from databases import contextos

# Importamos las rutas
from security.routes import security_bp
from home.routes import home_bp 
from api.routes import api_bp
from chat.routes import chat_bp
from notify.routes import notify_bp
from configs.routes import configs_bp
from widget.routes import widget_bp

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

@app.before_request
def load_context():
    contextos.load_context_values()

# Middleware
@app.before_request
def restrict_by_ip():
    # Obtén la ruta actual
    current_path = request.path

    # Lista de IPs permitidas para la aplicación widget
    widget_ips = ['127.0.0.1']

    # Si la ruta corresponde a la aplicación widget, no verificamos la IP
    if current_path.startswith('/widget'):
        return

    # En caso contrario, verificamos la IP
    list_ips = ips.get_ips() + widget_ips
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    if client_ip not in list_ips:
        abort(403)

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
app.register_blueprint(widget_bp)

if __name__ == "__main__":
    debug = os.environ.get('DEBUG')
    app.run(
        debug=debug,
        host="0.0.0.0",
        port=5000
    )