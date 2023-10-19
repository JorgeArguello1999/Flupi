from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Variable para ver el estado del trabajo
work = {
    "status": False
}

# Configuración de dirección del servidor
host = "192.168.11.12"
port = 8080

@app.route("/")
def home():
    return render_template('index.html', host=host, port=port)

@app.route("/chatbot", methods=["GET"])
def chatbot_message():
    return jsonify({
        "status": work["status"]
    })

@app.route("/chatbot/<int:statuswork>", methods=["GET"])
def chatbot_message_give(statuswork):
    status = False
    if statuswork == 1:
        status = True

    work["status"] = status
    
    return jsonify({
        "status": "changed"
    })

if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)
