from firebase_admin import credentials, firestore
from dotenv import load_dotenv

import os 
import firebase_admin

load_dotenv()

# Configuración inicial
ruta = os.environ.get('JSON_GCS')
nombre = os.environ.get('NOMBRE')

# Inicializa la app de Firebase
cred = credentials.Certificate(ruta)
firebase_admin.initialize_app(cred)

def get_context(key:str, coleccion='contextos') -> str:
    db = firestore.client()
    try:
        collecion = db.collection(coleccion)
        documentos = collecion.stream()
        data_dict = {documento.id: documento.to_dict().get(key) for documento in documentos if key in documento.to_dict()}
        return data_dict[nombre]

    except Exception as e:
        return f'Error: {e}'

if __name__ == "__main__":
    print(get_context('no_producto'))