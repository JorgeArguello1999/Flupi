from firebase_admin import credentials, firestore
from dotenv import load_dotenv

import firebase_admin
import os

load_dotenv()

class Users:
    def __init__(self):
        self.ruta_tokens = os.getenv('JSON_GCS')
        self.cred = credentials.Certificate(self.ruta_tokens)
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()

    def get_users(self, coleccion_padre, doc_id, subcoleccion):
        try:
            doc_ref = self.db.collection(coleccion_padre).document(doc_id)
            subcoleccion_ref = doc_ref.collection(subcoleccion).stream()

            # Realizar operaciones con los documentos dentro de la subcolección
            salida = {}
            for doc in subcoleccion_ref:
                salida[doc.id] = doc.to_dict()

            return salida

        except Exception as e:
            print(f"Error al acceder a la subcolección: {e}")
            return False

    def create_user(self, coleccion_padre, doc_id, subcoleccion, datos):
        try:
            doc_ref = self.db.collection(coleccion_padre).document(doc_id)
            subcoleccion_ref = doc_ref.collection(subcoleccion)
            
            # Crear un nuevo documento dentro de la subcolección
            nuevo_doc_ref = subcoleccion_ref.document()
            nuevo_doc_ref.set(datos)
            
            print("Documento creado exitosamente en la subcolección.")
            return nuevo_doc_ref.id
            
        except Exception as e:
            print(f"Error al crear el documento en la subcolección: {e}")
            return None
    
    def update_user(self, coleccion_padre, doc_id, subcoleccion, doc_sub_id, nuevos_datos):
        try:
            doc_ref = self.db.collection(coleccion_padre).document(doc_id)
            subcoleccion_ref = doc_ref.collection(subcoleccion)
            
            # Actualizar un documento específico dentro de la subcolección
            doc_ref = subcoleccion_ref.document(doc_sub_id)
            doc_ref.update(nuevos_datos)
            
            print(f"Documento con ID '{doc_sub_id}' actualizado en la subcolección.")
            return True
            
        except Exception as e:
            print(f"Error al actualizar el documento en la subcolección: {e}")
            return False

    def delete_user(self, coleccion_padre, doc_id, subcoleccion, doc_sub_id):
        try:
            doc_ref = self.db.collection(coleccion_padre).document(doc_id)
            subcoleccion_ref = doc_ref.collection(subcoleccion)
            
            # Eliminar un documento específico dentro de la subcolección
            subcoleccion_ref.document(doc_sub_id).delete()
            
            print(f"Documento con ID '{doc_sub_id}' eliminado de la subcolección.")
            return True
            
        except Exception as e:
            print(f"Error al eliminar el documento de la subcolección: {e}")
            return False

if __name__ == '__main__':
    firestore_crud = Users()

    salida = firestore_crud.get_users('contextos', 'Compumax', 'usuarios')
    print(salida)

    usuarios = {"username": 'jorge', "password": "Hola"}
    salida = firestore_crud.create_user('contextos', 'Compumax', 'usuarios', usuarios)
    print(salida)