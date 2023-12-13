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
        messages= [
            {"role": "system", "content": context},
            {"role": "user", "content": ask}
        ],
        temperature=0
    )

    response = response.choices[0].message

    return {
        "response": response.content
    }

# Esta parte es para pruebas
if __name__ == '__main__':
    import context

    contexto = context.entender_consulta
    ask="Usuario: Tienes teclados?"
    user = "Jorge"
    salida = answer(
        context=contexto,
        user=user,
        ask=ask,
    )
    print(salida)