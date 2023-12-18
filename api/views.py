from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import datetime
import json

from .models import Contextos

from . import chatbot
from . import chatgpt
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

@csrf_exempt
def api_post(request):
    if request.method == "POST" and request.content_type == 'application/json':
        try:
            data = json.loads(request.body)

            # Obtenemos la hora de Petición
            hora_peticion =  datetime.datetime.now().strftime('%H:%M')

            # Consultamos a la base de datos
            entender_consulta = Contextos.objects.filter(name='entender_consulta').values()[0]
            contexto = Contextos.objects.filter(name='contexto').values()[0]

            # Enviamos a ChatGPT para que nos devuelva que pide el usuario
            response = chatgpt.answer(
                user= data["user"],
                ask= data["ask"],
                context= f"{entender_consulta} tu eres: {contexto}"
            )

            comandos = chatbot.chatbot(response["response"])

            # Se comprueba si se activo algún comando
            if comandos:
                response = comandos["response"]
            
            # Caso contrario se devuelve la respuesta de GPT 
            else:
                response = response["response"]

            if data["device"] == "bot":
                pass
                # response = voice.speaker(response)
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
        
        except Exception as e:
            response = ({
                "error": e
            })

        print(response)
    
    return JsonResponse(response)