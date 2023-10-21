from modules import voice, chatgpt, comandos, database
from server import server
from context import conf as context
import os, re, subprocess, signal
import requests

token = os.environ.get("GPT")
nombre = comandos.nombre
database = database.connect()

# Función de Escucha
def microfono():
    while True:
        # Abrimos el microfono a la escucha
        audio = voice.microphone()
        print(audio)
        # Buscamos dentro de lo detectado si activo un comando
        comando = comandos.functions(audio)

        # Comprobamos si dijo el nombre 
        if nombre in audio:
            # Comprobamos si ejecutamos algún comando
            if comando != None:
                voice.speaker(comando)
                continue

            # Verificamos si pregunto algún precio
            if "cuánto cuesta" in audio or "Cuánto cuesta" in audio:
                # Filtramos la entrada de voz
                id_product = ''.join(re.findall(r'\d', audio))
                # Respondemos la pregunta
                salida = database.search(int(id_product))
                salida = f"El {salida[0]} cuesta {salida[2]}"
                voice.speaker(salida)
                continue
            
            # Ofrecemos una descripción sobre el producto
            if "descripción" in audio:
                id_product = ''.join(re.findall(r'\d', audio))
                salida = database.search(int(id_product))
                prompt = f"""Voy a pasar datos de un producto, tu crea un pequeño 
                parrafo que lo describa, utiliza explicitamente solo la información 
                del texto, nada más: {salida}"""
                contexto = context.context(nombre=nombre, question=prompt)
                respuesta = chatgpt.answer(token=token, context=contexto)
                voice.speaker(respuesta)
                continue
            
            # Llamamos al técnico
            if "llama al técnico" in audio:
                ""
                voice.speaker("Espera un momento, puedes tomar asiento")
                requests.get()
                continue

            # Ejecutamos cualquier consulta en base al contexto
            else:
                # Preparamos la pregunta con nuestro context
                contexto = context.context(nombre=nombre, question=audio)
                respuesta = chatgpt.answer(token=token, context=contexto)
                voice.speaker(respuesta)

try:
    # Iniciar el proceso del servidor Flask
    server_process = subprocess.Popen("python3 modules/server.py", shell=True)

    # Hilo principal
    microfono()
except KeyboardInterrupt:
    # Para terminar el proceso del servidor Flask
    server_process.send_signal(signal.SIGTERM)
    server_process.wait()
