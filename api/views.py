from django.http import JsonResponse

#from .modules import context
#from .modules import chatbot
#from .modules import chatgpt
#from .modules import voice

import datetime

# Vistas de la API
def api_get(request):
    return JsonResponse({
        "formato": "JSON",
        "method": {
            "GET": "Esta página",
            "POST": "Interacción con la API"
        },
        "body_form": {
            "user": "Nombre del Usuario",
            "ask": "Pregunta del usuario",
            "device": "Computer o Bot"
        },
        "ejemplo": {
            "request_json": {
                "user": "Jorge",
                "ask": "Tienes teclados?",
                "device": "Computer"
            },
            "response_json": {
                "user": "Jorge",
                "ask": "Tienes teclados?",
                "role": "assistant",
                "response": "Datos",
                "time_answer": "00:01",
                "time_request": "00:01"
            }
        }
   })

"""
def api_post(request):
    # Obtenemos la hora de Petición
    hora_peticion =  datetime.datetime.now().strftime('%H:%M')
    # Obtenemos el JSON
    data = request.get_json()

    # Enviamos a ChatGPT para que nos devuelva que pide el usuario
    response = chatgpt.answer(
        user= data["user"],
        ask= data["ask"],
        context= f"{context.entender_consulta} tu eres: {context.context}"
    )

    comandos = chatbot.chatbot(response["response"])

    # Se comprueba si se activo algún comando
    if comandos:
        response = comandos["response"]
    
    # Caso contrario se devuelve la respuesta de GPT 
    else:
        response = response["response"]

    if data["device"] == "bot":
        response = voice.speaker(response)
        #return send_from_directory('static/audio_chatbot', response)

    # Obtenemos hora respuesta
    hora_respuesta =  datetime.datetime.now().strftime('%H:%M')

    # Salida de la API
    response = {
        "user": data["user"],
        "ask": data["ask"],
        "role": "assitant", 
        "response": response,
        "time_request": hora_peticion,
        "time_answer": hora_respuesta
    }

    return JsonResponse(response)
"""