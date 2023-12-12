import datetime, requests
try: 
    from modules import chatgpt, context, database
except:
    import chatgpt, context, database

# Aqui añadir más funciones al sistema de ser necesario

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
def get_product_description(text:str):
    func_words = "func database"
    texto = text.replace(func_words, "").strip()
    response = database.search_product(texto)

    contexto = context.caracteristicas_producto()
    response = chatgpt.answer(
        user="database",
        context=contexto,
        ask=texto
    )
    return response

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
    contexto = context.context(question=text)
    return chatgpt.answer(context=contexto)

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
            if command in text:
                return actions[command](text)
        return execute_query(text)
    
    except Exception as e:
        return f"Problema con la ejecución del comando: {text}"

if __name__ == "__main__":
    print(chatbot("La la la la func database teclados"))