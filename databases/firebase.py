from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import firebase_admin
import os

load_dotenv()

ruta_tokens = os.environ.get('JSON_GCS')
nombre = os.environ.get('NOMBRE')

# Inicializa la app de Firebase
cred = credentials.Certificate(ruta_tokens)
firebase_admin.initialize_app(cred)

def read_document(coleccion:str, key:str):
    db = firestore.client()
    try:
        coleccion_ref = db.collection(coleccion)
        documentos = coleccion_ref.stream()
        data_dict = {documento.id: documento.to_dict().get(key) for documento in documentos if key in documento.to_dict()}
        return data_dict[nombre]

    except Exception as e:
        return None

def list_all_documents(coleccion:str):
    db = firestore.client()
    try:
        coleccion_ref = db.collection(coleccion)
        documentos = coleccion_ref.stream()
        all_data = []

        for documento in documentos:
            all_data.append({documento.id: documento.to_dict()})
        
        return all_data

    except Exception as e:
        print(f"Error al obtener todos los documentos: {e}")
        return None


def delete_document(collection_name, document_id):
    db = firestore.client()
    try:
        doc_ref = db.collection(collection_name).document(document_id)
        doc_ref.delete()
        print(f"Documento '{document_id}' eliminado correctamente de la colección '{collection_name}'.")
    except Exception as e:
        print(f"Error al eliminar el documento: {e}")

if __name__ == '__main__':
    # Ejemplo de uso de las funciones
    # print(read_document('contextos', 'no_producto'))
    # print(read_document('contextos', 'mensajes'))
    #delete_document('edumax', '')
    print(list_all_documents('contextos'))
    # print(delete_document_by_id(input('ID: ')))