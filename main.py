from modules import voice, chatgpt, comandos, database, camera
from context import conf as context
import os, re, subprocess, multiprocessing
import requests

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

# Función de Escucha principal
def chatbot():
    while True:
        # Abrimos el microfono a la escucha
        audio = voice.microphone()
        # Buscamos dentro de lo detectado si activo un comando
        comando = comandos.functions(audio)
        # Vemos lo que dijo el usuario
        print(audio)

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
                
# Saluda a personas que conoce (Camara)
def start_camera():
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

# Iniciamos el servidor
def start_server():
    # Iniciar el proceso del servidor Flask
    server_process = subprocess.Popen(
        server_command, 
        shell=True, 
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL
    )
    server_process.wait()

def start_interface():
    # Iniciar el proceso del servidor Flask
    interface_process = subprocess.Popen(
        "python3 modules/interface.py",
        shell=True, 
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL
    )
    interface_process.wait()

"""
# Ejecutamos nuestro proyecto  
def start():
    # Hilo principal
    chatbot()

    # Hilo para el servidor Flask
    start_server()

    # Hilo para la interfaz gráfica
    start_interface()

    # Hilo para la ejecución de la camara
    # start_camera()
"""
if __name__ == "__main__":
    server_process = multiprocessing.Process(target=start_server)
    # camera_process = multiprocessing.Process(target=start_camera)
    interface_process = multiprocessing.Process(target=start_interface)
    chatbot_process = multiprocessing.Process(target=chatbot)

    server_process.start()
    # camera_process.start()
    interface_process.start()
    chatbot_process.start()

    server_process.join()
    # camera_process.join()
    interface_process.join()
    chatbot_process.join()


