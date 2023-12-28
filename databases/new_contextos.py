try:
    from databases import firestore
except:
    import firestore

# Iniciamos el objeto para contextos
contextos = firestore.Firestore()

def get_context_all() -> list:
    response = contextos.get_value('contextos', 'mensajes')

    if response:
        response = response.keys()
        return [ i for  i in response ]
    else:
        return ['Problema con la base de datos']

def get_context(key:str) -> str:
    response = contextos.get_value('contextos', 'mensajes')
    if response: 
        return response.get(key)
    else:
        return 'Error: Con la base de datos'

def update_context(name:str, text:str) -> bool:
    data = {f'mensajes.{name}':text }
    response = contextos.update_create_registry('contextos', data)
    return response


if __name__ == "__main__":
    # print(get_context('no_producto'))
    print(update_context('general', 'familia'))
    print(get_context('no_producto'))
