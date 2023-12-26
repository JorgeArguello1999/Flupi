from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import firebase_admin
import os

load_dotenv()

ruta_tokens = os.environ.get('JSON_GCS')

# Inicializa la app de Firebase
cred = credentials.Certificate(ruta_tokens)
firebase_admin.initialize_app(cred)

def read_document(collection_name, key):
    db = firestore.client()

    try:
        coleccion_ref = db.collection(collection_name)
        documentos = coleccion_ref.stream()
        data_dict = {documento.id: documento.to_dict().get(key) for documento in documentos if key in documento.to_dict()}
        return data_dict
    except Exception as e:
        print(f"Error: {e}")
        return None

def insert_document(collection_name, document_data):
    db = firestore.client()

    try:
        doc_ref = db.collection(collection_name).add(document_data)
        print(f"Documento agregado con ID: {doc_ref.id} en la colección '{collection_name}'")
        return doc_ref.id
    except Exception as e:
        print(f"Error al insertar el documento: {e}")
        return None

def update_document(collection_name, document_id, updated_data):
    db = firestore.client()

    try:
        doc_ref = db.collection(collection_name).document(document_id)
        doc_ref.update(updated_data)
        print(f"Documento con ID '{document_id}' en la colección '{collection_name}' actualizado exitosamente.")
        return True
    except Exception as e:
        print(f"Error al actualizar el documento: {e}")
        return False

def get_all_keys(collection_name):
    db = firestore.client()

    try:
        coleccion_ref = db.collection(collection_name)
        documentos = coleccion_ref.stream()
        keys_set = set()
        for documento in documentos:
            doc_data = documento.to_dict()
            keys_set.update(doc_data.keys())

        return list(keys_set)
    except Exception as e:
        print(f"Error: {e}")
        return None

def listar_todo_firestore():
    # Obtiene una instancia de Firestore
    db = firestore.client()

    try:
        # Obtiene todas las colecciones
        colecciones = [col.id for col in db.collections()]

        print("Colecciones almacenadas en Firestore:")
        for coleccion in colecciones:
            print(coleccion)

        return colecciones

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == '__main__':
    # Ejemplo de uso de las funciones
    """
    resultados = read_document('contextos', 'general')
    print(resultados)

    """
    claves = get_all_keys('contextos')
    print(claves)

    print(listar_todo_firestore())