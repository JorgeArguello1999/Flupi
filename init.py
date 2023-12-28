from firebase_admin import credentials, firestore
import firebase_admin

from dotenv import load_dotenv
import os

load_dotenv()

# Inicializa la aplicación de Firebase Admin
cred = credentials.Certificate(f'{os.getenv("JSON_GCS")}')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Estructura deseada que deseamos verificar
estructura = {
    "alarm": 0,
    "ips": ["192.168.11.114"],
    "fotos": {
        "chatbot": "foto_base64",
        "usuario": "foto_base64"
    },
    "mensajes": {
        "entender_consulta": "texto",
        "general": "texto",
        "no_producto": "texto"
    }
}

def initialize(database:str, proyect_name:str)-> bool:
    """
    Si existe devolvera True caso contrario creara y devolvera False
    """

    # Referencia al documento específico en la colección original
    documento_ref = db.collection(database).document(proyect_name)
    documento = documento_ref.get()

    if documento.exists:
        print('Estructura existe, no se hace nada')
        return True

    else:
        # Actualiza el documento original con la nueva estructura (sin 'usuarios')
        print('Creando estructura....')
        documento_ref.set(estructura)
        print('Seteando valores...')

        # Crea una subcolección 'usuarios' dentro del documento actual
        usuarios_ref = documento_ref.collection('usuarios')
        usuarios_ref.document().set({
            "username": "chatbot",
            "password": "scrypt:32768:8:1$tZDyvAfnpCFDfsNw$3de706a96f4088e5625a5386e9c08766da12589ccb390d62c6af547d9e2352a5db12beb6935b6a04f5aaf8619ff97dc2023e1c3608829c41f665f811ba72c26d",
            "token": "231c4d5a-eac0-4362-842d-3af49f4e4188"
        })
        print('Terminado.')

        return False

if __name__ == '__main__':
    salida = initialize('contextos', 'Edumax')
    print(salida)