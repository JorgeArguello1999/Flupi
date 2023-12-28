import base64

try:
    from databases import FireStoreBase
except:
    import FireStoreBase

# Iniciamos el objeto para imagenes
imagenes = FireStoreBase.Firestore('imagenes')

def get_image_all() -> list:
    response = imagenes.get_value('fotos')
    data = [ i for i in response.keys() ]
    return data

def get_image(filename:str):
    response = imagenes.get_value('fotos')
    salida = response.get(filename)
    salida = base64.b64encode(salida).decode('utf-8')
    return salida 

def update_image(filename:str, image) -> bool:
    data = {f'fotos.{filename}': image}
    return imagenes.update_create_registry(data)

if __name__ == '__main__':
    print(get_image_all())
    print(get_image('chatbot'))
    print(update_image('chatbot', '8'))