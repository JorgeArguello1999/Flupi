from flask import send_from_directory
from flask import jsonify

from configs import api_compumax
from configs import chatgpt
from configs import chatbot
from configs import voice

from databases import contextos

from datetime import datetime

# Obtener el tiempo del servidor
def get_current_time():
    return datetime.now().strftime('%H:%M')

# Respuesta Texto
def computer(data_user:dict, only_response=False) -> dict:
    # Hora de inicio de la petición
    hora_inicio = get_current_time()

    # Enviamos a ChatGPT para que nos devuelva lo que pide el usuario
    chat_response = chatgpt.answer(
        user=data_user["user"],
        ask=data_user["ask"],
        context=f"{contextos.get_context('entender_consulta')} {contextos.get_context('general')}"
    )

    comandos = chatbot.chatbot(chat_response["response"])

    # Se comprueba si se activó algún comando
    response = comandos["response"] if comandos else chat_response["response"]

    # Enviamos solo la respuesta del modelo
    if only_response == True:
        return response

    # Salida de la API
    return jsonify({
        "user": data_user["user"],
        "ask": data_user["ask"],
        "role": "assistant",
        "response": response,
        "time_request": hora_inicio, 
        "time_answer": get_current_time() 
    })

# Respuesta Voz
def bot(data_user:dict):
    response = computer(data_user=data_user, only_response=True)
    response = voice.speaker(response)
    return send_from_directory('./audios', response)

# Respuesta directa
def productos(data_user:dict):
    # Hora de inicio de la petición
    hora_inicio = get_current_time()

    # En caso de que envíe solo dígitos
    response = api_compumax.search_product(data_user['ask'])

    # Salida de la API
    return jsonify({
        "user": data_user["user"],
        "ask": data_user["ask"],
        "role": "assistant",
        "response": response,
        "time_request": hora_inicio,
        "time_answer": get_current_time() 
    })

