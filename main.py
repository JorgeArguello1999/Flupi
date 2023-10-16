from modules import voice_text, text_voice, chatgpt, comandos, database
from context import conf as context
import os, re 

token = os.environ.get("GPT")
nombre = comandos.nombre
database = database.connect()

while True:
    # Abrimos el microfono a la escucha
    audio = voice_text.microphone()
    print(audio)
    # Buscamos dentro de lo detectado si activo un comando
    comando = comandos.functions(audio)

    # Comprobamos si dijo el nombre 
    if nombre in audio:
        # Comprobamos si ejecutamos algún comando
        if comando != None:
            text_voice.speaker(comando)

        # Verificamos si pregunto algún precio
        if f"{nombre} cuánto cuesta" in audio or f"{nombre} Cuánto cuesta" in audio:
            # Filtramos la entrada de voz
            id_product = ''.join(re.findall(r'\d', audio))
            respuesta = database.search(int(id_product))

        # Ejecutamos cualquier consulta en base al contexto
        else:
            # Preparamos la pregunta con nuestro context
            contexto = context.clean(nombre=nombre, question=audio)
            respuesta = chatgpt.answer(token=token, context=contexto)
            text_voice.speaker(respuesta)

