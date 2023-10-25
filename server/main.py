from flask import Flask, jsonify, render_template
from flask import redirect, url_for
from flask_cors import CORS
import sys

class Servidor:
    def __init__(self, host:str, port:int):
        """
        :host -> IP para que corra el servidor
        :port -> Puerto para exponer la API
        """
        # Configuraciones del servidor
        self.app = Flask(__name__)
        CORS(self.app)
        self.app.config["STATIC_URL"] = "/static"

        # Configuración de dirección del servidor
        self.host = host
        self.port = port

        # Variable para ver el estado del trabajo
        self.work = {
            "status": False
        }

        # Definir rutas
        self.app.add_url_rule("/", 'home', self.home)
        self.app.add_url_rule("/chatbot", 'chatbot_message', self.chatbot_message, methods=["GET"])
        self.app.add_url_rule("/chatbot/<int:statuswork>", 'chatbot_message_give', self.chatbot_message_give, methods=["GET", "POST"])

    def home(self):
        return render_template('index.html', host=self.host, port=self.port)

    def chatbot_message(self):
        try:
            return jsonify({
                "status": self.work["status"]
            })
        except Exception as error:
            print(error)
            return jsonify({
                "error": error
            })

    def chatbot_message_give(self, statuswork):
        status = False
        if statuswork == 1:
            status = True

        self.work["status"] = status
        return redirect(url_for('home'))
        
    def start(self):
        self.app.run(host=self.host, port=self.port, debug=True)

if __name__ == "__main__":
    # Obtenemos los parametros para ejecutar el modulo
    host = sys.argv[1]
    port = sys.argv[2]
    app = Servidor(
        host=host,
        port=port
    )
    app.start()
