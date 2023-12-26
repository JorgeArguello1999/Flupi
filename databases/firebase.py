from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import firebase_admin
import os

load_dotenv()

ruta_tokens = os.environ.get('JSON_GCS')
nombre = os.environ.get('NOMBRE')
coleccion = 'contextos'

# Inicializa la app de Firebase
cred = credentials.Certificate(ruta_tokens)
firebase_admin.initialize_app(cred)

def read_document(key):
    db = firestore.client()
    try:
        coleccion_ref = db.collection(coleccion)
        documentos = coleccion_ref.stream()
        data_dict = {documento.id: documento.to_dict().get(key) for documento in documentos if key in documento.to_dict()}
        return data_dict[nombre]

    except Exception as e:
        return None

if __name__ == '__main__':
    # Ejemplo de uso de las funciones
    resultados = read_document('general')
    print(resultados)