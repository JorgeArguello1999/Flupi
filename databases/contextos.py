from firebase_admin import credentials, firestore
from dotenv import load_dotenv

import os 
import firebase_admin

load_dotenv()

# Configuración inicial
ruta = os.environ.get('JSON_GCS')
nombre = os.environ.get('NOMBRE')
coleccion = 'contextos'

# Inicializa la app de Firebase
cred = credentials.Certificate(ruta)
firebase_admin.initialize_app(cred)

def get_context_all() -> list:
    return ["no_producto", "error_mensaje", "general", "entender_consulta"]

def get_context(key:str, coleccion=coleccion) -> str:
    db = firestore.client()
    try:
        data = db.collection(coleccion)
        documentos = data.stream()
        data_dict = {documento.id: documento.to_dict().get(key) for documento in documentos if key in documento.to_dict()}
        return data_dict[nombre]

    except Exception as e:
        return f'Error: {e}'

def update_context(name: str, text:str) -> bool:
    db = firestore.client()
    try:
        # Actualiza el valor de 'no_producto' dentro del documento 'compumax' en la colección 'contextos'
        ref = db.collection(coleccion).document(nombre)
        data = ref.get().to_dict() 
        if data:
            ref.update({name: text})
            return True
        else:
            return False

    except Exception as e:
        print(f"Error al actualizar el valor de 'no_producto': {e}")
        return False

# Ejemplo de uso:
if __name__ == "__main__":
    print(get_context('no_producto'))
    print(update_context('no_producto', 'Ha'))
    print(get_context('no_producto'))