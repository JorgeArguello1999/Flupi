from openai import OpenAI
import google.generativeai as genai

import json

from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv('API_KEY')

# Enviamos el Token de Verificacion

def answer(user:str="anonym", context:str="", ask:str="") -> json:
    genai.configure(api_key=key) 
    """
    :param context contexto para responder la pregunta
    :param user nombre o IP de la persona que pregunta
    :param ask pregunta del usuario
    """
    model = genai.GenerativeModel(
        'gemini-pro',
        safety_settings={'HARASSMENT': 'block_none'},
        generation_config={
            "temperature": 1,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 1024
        }
    )

    chat = model.start_chat(history=[])
    combined_input = context + "\n" + ask 
    response = chat.send_message(combined_input, stream=True)
    response.resolve()

    if response:
        respuesta_completa = ''.join(chunk.text for chunk in response)
    else:
        respuesta_completa = "No se recibió respuesta del modelo."

    print(f"\nBot: {respuesta_completa}")
    return {"response": respuesta_completa}

if __name__ == '__main__':
    salida = answer()
    print(salida)