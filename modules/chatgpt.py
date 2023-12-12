import openai

def answer(token:str, context:str):
    """
    :param context is a query
    """
    # Enviar una solicitud al modelo para generar texto
    openai.api_key = token 
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=context,
        max_tokens=250
    ).choices[0].text

    return response
    
if __name__ == '__main__':
    salida = answer(
        input('Insert a token: '),
        'Hola mundo en sql'
    )
    print(salida)