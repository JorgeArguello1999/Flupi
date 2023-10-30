from modules import voice, chatgpt, comandos, database, camera
from context import conf as context
import os, re, subprocess, signal
import requests
import queue

# Cola dondo colocamos nuestros mensajes
comunicacion = queue.Queue()

# Variables de entorno
token = os.environ.get("GPT")
nombre = comandos.nombre

# Conexión a la base de articulos
articulos = database.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    passwd="root",
    db="articulos"
)
# Creación del servidor web
server_host = "192.168.11.12"
server_port = 8080
server_command = f"python server/main.py {server_host} {server_port}"

# Función de Escucha
def microfono():
    while True:
        # Abrimos el microfono a la escucha
        audio = voice.microphone()
        # Buscamos dentro de lo detectado si activo un comando
        comando = comandos.functions(audio)
        # Vemos lo que dijo el usuario
        print(audio)

        # Comprobamos si dijo el nombre 
        if nombre in audio:
            # Enviamos mensaje a la interfaz
            comunicacion.put("True")

            # Comprobamos si ejecutamos algún comando
            if comando != None:
                voice.speaker(comando)
                continue

            # Verificamos si pregunto algún precio
            if "cuánto cuesta" in audio or "Cuánto cuesta" in audio:
                # Filtramos la entrada de voz
                id_product = ''.join(re.findall(r'\d', audio))
                # Respondemos la pregunta
                salida = articulos.search(int(id_product))
                salida = f"El {salida[0]} cuesta {salida[2]}"
                voice.speaker(salida)
                continue
            
            # Ofrecemos una descripción sobre el producto
            if "descripción" in audio:
                id_product = ''.join(re.findall(r'\d', audio))
                salida = articulos.search(int(id_product))
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
                try:
                    salida = requests.get(
                        url=f"http://{server_host}:{server_port}/chatbot/1"
                    )
                    print(f"url: {salida}")
                    voice.speaker("Espera un momento, puedes tomar asiento")
                except Exception as error:
                    voice.speaker("Ocurrió un error, Acercate al personal para solicitar la ayuda")
                    print(f"Error al llamar al técnico: {error}")

                continue

            # Ejecutamos cualquier consulta en base al contexto
            else:
                # Preparamos la pregunta con nuestro context
                contexto = context.context(nombre=nombre, question=audio)
                respuesta = chatgpt.answer(token=token, context=contexto)
                voice.speaker(respuesta)

        else:
            comunicacion.put("False")

# Saluda a personas que conoce
def saludar():
    """
    Devuelve un True cuando reconoce a alguien, y un False cuando no reconoce a nadie
    """
    salida = camera.recognite()
    if salida != "Desconocido":
        voice.speaker(f"¡Hola {salida}! Bienvenido a CompuMax ")
        return True
    else:
        voice.speaker(f"¡Hola!, Bienvenido a Compumax")
        return False

# Ejecutamos nuestro proyecto  
def start():
    try:
        # Iniciar el proceso del servidor Flask
        server_process = subprocess.Popen(
            server_command, 
            shell=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )

        # Hilo principal
        microfono()

    except KeyboardInterrupt:
        # Para terminar el proceso del servidor Flask
        server_process.send_signal(signal.SIGTERM)
        server_process.wait()

if __name__ == "__main__":
    start()