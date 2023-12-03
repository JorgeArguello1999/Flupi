from modules import voice, chatgpt, database
from context import conf as context
import os, re, datetime
import requests
from dotenv import load_dotenv

# Variables de entorno
load_dotenv()
token = os.environ.get("GPT")

# Conexión a la base de articulos
articulos = database.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    passwd="root",
    db="articulos"
)

# Aqui van los comandos
nombre = "Maxi"
hora = datetime.datetime.now().strftime("%H:%M")
fecha_actual = datetime.datetime.now()
nombres_meses = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio", 
    8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}
fecha = f"{fecha_actual.day} de {nombres_meses[fecha_actual.month]} de {fecha_actual.year}"
comandos = {
    f"Hola {nombre}": "Hola, en que te puedo ayudar?",
    f"{nombre} qué hora es": f"Hola, la hora es: {hora}",
    f"{nombre} qué fecha es": f"La fecha es: {fecha}"
}

def functions(text:str):
    for com in comandos:
        if text in com:
            return comandos[com]


# Este es el modulo de ejecución principal
def chatbot(text:str, server_host="127.0.0.1", server_port=5000)->str:
    # Buscamos dentro de lo detectado si activo un comando
    comando = functions(text)
    # Vemos lo que dijo el usuario
    print(text)

    # Comprobamos si ejecutamos algún comando
    if comando != None:
        return comando
            
    # Verificamos si pregunto algún precio
    if "cuánto cuesta" in text or "Cuánto cuesta" in text:
        # Filtramos la entrada de voz
        id_product = ''.join(re.findall(r'\d', text))
        # Respondemos la pregunta
        salida = articulos.search(int(id_product))
        return f"El {salida[0]} cuesta {salida[2]}"
           
    # Ofrecemos una descripción sobre el producto
    if "descripción" in text:
        id_product = ''.join(re.findall(r'\d', text))
        id_producto = articulos.search(int(id_product))
        prompt = context.caracteristicas_producto(id_producto)
        contexto = context.context(nombre=nombre, question=prompt)
        return chatgpt.answer(token=token, context=contexto)
            
    # Llamamos al técnico
    if "llama al técnico" in text:
        try:
            requests.get(
                url=f"http://{server_host}:{server_port}/notify/1"
            )
            return "Espera un momento, puedes tomar asiento"
        except Exception as error:
            print(f"Error al llamar al técnico: {error}")
            return context.error_mensaje() 

    # Ejecutamos cualquier consulta en base al contexto
    else:
        # Preparamos la pregunta con nuestro context
        contexto = context.context(nombre=nombre, question=text)
        respuesta = chatgpt.answer(token=token, context=contexto)
        return respuesta

if __name__ == "__main__":
    salida = chatbot("dame una descripción del 7092")
    voice.speaker(salida)