from flask import Flask
from flask_cors import CORS

import os

# Importamos las rutas
from home.routes import home_bp 
from api.routes import api_bp

app = Flask(__name__)
CORS(app)

# Registramos las rutas
app.register_blueprint(home_bp)
app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run(
        debug=os.environ.get("DEBUG"),
        host="0.0.0.0",
        port=5000
    )
