from modules import voice, chatgpt, comandos, database
from modules import server
from context import conf as context
import os, re, threading, socket

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
                send_message(text="Cliente afuera!!!", username=nombre)
                voice.speaker("Espera un momento, puedes tomar asiento")
                continue

            # Ejecutamos cualquier consulta en base al contexto
            else:
                # Preparamos la pregunta con nuestro context
                contexto = context.context(nombre=nombre, question=audio)
                respuesta = chatgpt.answer(token=token, context=contexto)
                voice.speaker(respuesta)


def send_message(username:str, text:str)-> bool:
    """
    :username -> Nombre de usuario
    :text -> Texto a enviar
    Return True or False
    """
    # Variables cliente
    host = server.host
    port = server.port
    print(host, port)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    try:
        message = f"{username}: {text}"
        client.send(message.encode('utf-8'))
        print("Mensaje enviado")
        return True
    except Exception as error:
        print(f"Error: {error}")
        return False

# Abrimos hilos
microfono_thread = threading.Thread(target=microfono)
servidor_thread = threading.Thread(target=server.create_server)

# Iniciamos los hilos
microfono_thread.start()
servidor_thread.start()

# Terminamos los hilos
microfono_thread.join()
servidor_thread.join()
