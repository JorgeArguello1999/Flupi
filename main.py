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
        if "cuánto cuesta" in audio or "Cuánto cuesta" in audio:
            # Filtramos la entrada de voz
            id_product = ''.join(re.findall(r'\d', audio))
            # Respondemos la pregunta
            salida = database.search(int(id_product))
            salida = f"El {salida[0]} cuesta {salida[2]}"
            text_voice.speaker(salida)
        
        # Ofrecemos una descripción sobre el producto
        if "descripción" in audio:
            id_product = ''.join(re.findall(r'\d', audio))
            salida = database.search(int(id_product))
            prompt = f"""Voy a pasar datos de un producto, tu crea un pequeño parrafo que 
            lo describa, utiliza explicitamente solo la información del texto, nada más: {salida}"""
            contexto = context.context(nombre=nombre, question=prompt)
            respuesta = chatgpt.answer(token=token, context=contexto)
            text_voice.speaker(respuesta)

        # Ejecutamos cualquier consulta en base al contexto
        else:
            # Preparamos la pregunta con nuestro context
            contexto = context.context(nombre=nombre, question=audio)
            respuesta = chatgpt.answer(token=token, context=contexto)
            text_voice.speaker(respuesta)
