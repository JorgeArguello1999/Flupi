try:
    from databases import FireStoreBase
except:
    import FireStoreBase

# Iniciamos el objeto para contextos
contextos = FireStoreBase.Firestore('contextos')

# Variables globales para almacenar los valores de la base de datos
context_all_values = []  # Almacena todos los valores
context_values = {}      # Almacena los valores por clave

# Función para cargar los valores de la base de datos en las variables globales
def load_context_values():
    global context_all_values
    global context_values

    response = contextos.get_value('mensajes')

    if response:
        context_all_values = list(response.keys())
        context_values = response
    else:
        context_all_values = ['Problema con la base de datos']
        context_values = {}

def get_context_all() -> list:
    return context_all_values

def get_context(key:str) -> str:
    return context_values.get(key, 'Error: Con la base de datos')

def update_context(name:str, text:str) -> bool:
    data = {f'mensajes.{name}': text}
    response = contextos.update_create_registry(data)
    if response:
        # Si la actualización fue exitosa, actualiza las variables globales
        load_context_values()
    return response

if __name__ == "__main__":
    # Cargar los valores de la base de datos en las variables globales al inicio
    load_context_values()
    print(get_context_all())
    # print(update_context('general', 'amilia'))
    print(get_context('general'))

else:

    load_context_values()
    print(get_context_all())