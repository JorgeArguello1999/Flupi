from modules import voice_text, text_voice, chatgpt, comandos
from context import conf as context
import os 

token = os.environ.get("GPT")
nombre = comandos.nombre

while True:
    # Abrimos el microfono a la escucha
    voz = voice_text.microphone()
    print(voz)
    # Buscamos dentro de lo detectado si activo un comando
    comando = comandos.functions(voz)

    # Comprobamos si dijo el nombre 
    if nombre in voz:
        if comando != None:
            text_voice.speaker(comando)
        else:
            # Preparamos la pregunta con nuestro context
            contexto = context.clean(nombre=nombre, question=voz)
            respuesta = chatgpt.answer(token=token, context=contexto)
            text_voice.speaker(respuesta)