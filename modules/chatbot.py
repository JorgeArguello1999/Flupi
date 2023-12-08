import datetime, os, re, requests
from modules import chatgpt, context, database
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get("GPT")

"""
Aquí se realizan cada uno de los comandos como funciones, estas funciones
deben devolver siempre un <<String>>, y aparte tienes que añadirlas a un 
diccionario en la parte inferior para que funcionen
"""

# Saludo
def greet(trash):
    return f"Hola, en que te puedo ayudar?"

# Hora
def get_time(trash):
    return f"Hola, la hora es: {datetime.datetime.now().strftime('%H:%M')}"

# Fecha
def get_date(trash):
    fecha_actual = datetime.datetime.now()
    nombres_meses = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio",
        8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    fecha = f"{fecha_actual.day} de {nombres_meses[fecha_actual.month]} de {fecha_actual.year}"
    return f"La fecha es: {fecha}"

# Producto - Descripción 
def get_product_description(text):
    id_product = ''.join(re.findall(r'\d', text))
    id_producto = database.search_product_by_id(int(id_product))
    prompt = context.caracteristicas_producto(id_producto)
    contexto = context.context(nombre="Maxi", question=prompt)
    return chatgpt.answer(token=token, context=contexto)

# Llamar al técnico
def call_technician(trash, server_host="0.0.0.0", server_port=5000):
    try:
        requests.get(
            url=f"http://{server_host}:{server_port}/notify/1"
        )
        return "Espera un momento, puedes tomar asiento"
    except Exception as error:
        print(f"Error al llamar al técnico: {error}")
        return context.error_mensaje() 

# Ejecutar cualquier consulta fuera de los comandos
def execute_query(text):
    contexto = context.context(nombre="Maxi", question=text)
    return chatgpt.answer(token=token, context=contexto)

"""
En esta parte de aquí podemos colocar las frases que activaran los comandos,
esta es más importante para los comandos con voz, en la versión web, tienes un 
desplegable donde solo seleccionas la opción y ya tienes una respuesta
"""

actions = {
    "Hola Maxi": greet,
    "Maxi qué hora es": get_time,
    "Maxi qué fecha es": get_date,
    "cuánto cuesta": get_product_description,
    "Cuánto cuesta": get_product_description,
    "descripción": get_product_description,
    "llama al técnico": call_technician
}

def chatbot(text:str)->str:
    try:
        for command in actions:
            if command in text:
                return actions[command](text)
        return execute_query(text)
    
    except Exception as e:
        return f"Problema con la ejecución del comando: {text}"

if __name__ == "__main__":
    print(chatbot("Hola Maxi"))