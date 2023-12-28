from firebase_admin import credentials, firestore
from dotenv import load_dotenv

import firebase_admin
import json
import os

load_dotenv()

class Firestore:
    def __init__(self):
        self.ruta_tokens = os.getenv('JSON_GCS')
        self.cred = credentials.Certificate(self.ruta_tokens)
        firebase_admin.initialize_app(self.cred)
        self.proyecto = os.environ.get('NOMBRE')
        self.proyecto = 'Compumax'
        self.db = firestore.client()

    # Obtener todo el Diccionario
    def get_all(self, coleccion:str) -> json:
        try:
            docs = self.db.collection(coleccion).stream()

            datos_coleccion = {}
            for doc in docs:
                datos_coleccion[doc.id] = doc.to_dict()

            # Convertir el diccionario a formato JSON
            return datos_coleccion[self.proyecto]

        except Exception as e:
            return json.dumps({'error': f'Error: {e}'}, indent=2)

    # Obtener solo un campo del Diccionario
    def get_value(self, coleccion:str, campo:str) -> json:
        try:
            docs = self.db.collection(coleccion).stream()

            datos_coleccion = {}
            for doc in docs:
                datos_coleccion[doc.id] = doc.to_dict().get(campo)
            
            return datos_coleccion[self.proyecto]

        except Exception as e:
            print(f"Error al buscar documentos: {e}")
            return []

    # Crea una coleccion
    def create_collection(self, coleccion:str, datos:json) -> bool:
        try:
            doc_ref = self.db.collection(coleccion).document()
            doc_ref.set(datos)
            print(f"Documento {doc_ref.id} creado exitosamente.")
            return True
            
        except Exception as e:
            print(f"Error al crear el documento: {e}")
            return False

    # Actualizar o crear un Campo
    def update_create_registry(self, coleccion:str, nuevos_datos:json) -> bool:
        try:
            doc_ref = self.db.collection(coleccion).document(self.proyecto)
            doc_ref.update(nuevos_datos)
            print(f"Documento con ID '{self.proyecto}' actualizado exitosamente.")
            return True

        except Exception as e:
            print(f"Error al actualizar el documento: {e}")
            return False

    # Eliminar un documento
    def delete_document(self, coleccion:str, doc_id:str) -> bool:
        try:
            doc_ref = self.db.collection(coleccion).document(doc_id)
            doc_ref.delete()
            print(f"Documento con ID '{doc_id}' eliminado exitosamente.")
            return True

        except Exception as e:
            print(f"Error al eliminar el documento: {e}")
            return False
    
    # Eliminar campo
    def delete_value(self, coleccion:str, campo:str) -> bool:
        try:
            doc_ref = self.db.collection(coleccion).document(self.proyecto)

            # Actualizar el campo que deseas eliminar con firebase_admin.firestore.DELETE_FIELD
            doc_ref.update({campo: firebase_admin.firestore.DELETE_FIELD})

            print(f"Campo '{campo}' del documento con ID '{self.proyecto}' eliminado exitosamente.")
            return True

        except Exception as e:
            print(f"Error al eliminar el campo: {e}")
            return False

if __name__ == '__main__':
    firestore_crud = Firestore()

    # Ejemplos de uso:
    # Buscar documentos en una colección filtrando por un campo y valor específicos
    listar = firestore_crud.get_all('contextos')
    print(listar)

    # Crear un nuevo documento en una colección con los datos proporcionados
    nuevo_doc_datos = {'campo1': 'valor1', 'campo2': 'valor2'}
    nuevo_doc_id = firestore_crud.create_collection('contextos', nuevo_doc_datos)

    # Actualizar un documento existente en una colección con nuevos datos
    datos_actualizados = {'alarm': False}
    firestore_crud.update_create_registry('contextos', 'Compumax', datos_actualizados)

    # Eliminar un documento por su ID de una colección específica

    firestore_crud.eliminar_campo('contextos', 'Compumax', 'prueba')