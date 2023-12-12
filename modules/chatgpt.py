from dotenv import load_dotenv
from openai import OpenAI
import os
load_dotenv()

# Enviamos el Token de Verificacion
client = OpenAI(api_key=os.environ.get("GPT"))

def answer(user:str="anonym", context:str="", ask:str=""):
    """
    :param context contexto para responder la pregunta
    :param user nombre o IP de la persona que pregunta
    :param ask pregunta del usuario
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages= [{
            "role": "user",
            "content": f"{context} {ask}"
        }],
        temperature=0
    )

    response = response.choices[0].message

    return {
        "user": user,
        "ask": ask,
        "role": response.role,
        "response": response.content
    }

if __name__ == '__main__':
    context = """
El cliente está preguntando por un producto específico. Asegúrate de proporcionar una respuesta que indique una búsqueda en la base de datos con el nombre del producto. Escribe una instrucción: "func database <producto>". Reemplaza "<producto>" con el nombre real del producto que el cliente está preguntando. Por ejemplo, si el cliente pregunta por "zapatillas deportivas", la instrucción resultante debería ser "func database zapatillas deportivas".
El cliente cuando solicite información de la hora vas a escribir "func time" en cualquier tipo de petición donde te pida el tiempo actual, por ejemplo "¿Que hora es?" tu respuesta va a ser "func time", lo mismo si dice que horas son, y así sucesivamente 
Cuando el cliente diga algo como "llamar al técnico" o "quiero llamar al técnico", o frases similares vas a responder de la siguiente manera "func tecnico", por ejemplo "llamar al técnico" tu respuesta debe ser "func tecnico", esto siempre y cuando su pregunta sea relacionada con ver al técnico
"""
    ask="Usuario: Tienes teclados?"
    user = "Jorge"
    salida = answer(
        context=context,
        user=user,
        ask=ask,
    )
    print(salida)