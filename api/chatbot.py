from django.urls import reverse

import datetime, requests

from . import api_soporte
from . import chatgpt

from .models import Contextos

# Aqui añadir más funciones al sistema de ser necesario

# Saludo
def greet(trash):
    return {
        "response": "Hola, en que te puedo ayudar?"
    }

# Hora
def get_time(trash):
    return {
        "response": f"Hola, la hora es: {datetime.datetime.now().strftime('%H:%M')}"
    }

# Fecha
def get_date(trash):
    fecha_actual = datetime.datetime.now()
    nombres_meses = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio",
        8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    fecha = f"{fecha_actual.day} de {nombres_meses[fecha_actual.month]} de {fecha_actual.year}"
    return {
        "response": f"La fecha es: {fecha}" 
    } 

# Producto - Descripción 
def get_product_description(text:str):
    func_words = "func database"
    texto = text.replace(func_words, "").strip()
    response = api_soporte.search_product(texto)

    no_producto = Contextos.objects.filter(name='no_producto').values()[0]
    contexto = Contextos.objects.filter(name="contexto").values()[0]

    if response != False:
        return {"response": response}
    
    else:
        return {
            "response": chatgpt.answer(
                ask=contexto,
                context=no_producto
            )["response"]
        }

# Llamar al técnico
def call_technician(trash):
    error_message = Contextos.objects.filter(name='error_message').values()[0]['content']
    try:
        requests.get("http://127.0.0.1:8000/notify/entry/1")
        message = "Espera un momento, puedes tomar asiento"
    except Exception as error:
        print(f"Error al llamar al técnico: {error}")
        message = str(error_message)  # Convirtiendo el mensaje de error a cadena de texto
    
    return {
        "response": message
    }

# Diferentes palabras que activan diferentes funciones
# Estas palabras estan configuradas en el context
# Revisar el context.py para más información
actions = {
    "func greet": greet,
    "func time": get_time,
    "func date": get_date,
    "func database": get_product_description,
    "func tecnico": call_technician
}

def chatbot(text:str)->str:
    try:
        for command in actions:
            if command.lower() in text:
                return actions[command](text)
        return False
    
    except Exception as e:
        return f"Problema con la ejecución del comando: {text}"

if __name__ == "__main__":
    print(chatbot("func database laptop"))