from firebase_admin import credentials, firestore
from dotenv import load_dotenv

import firebase_admin

try:
    from databases import FireStoreBase
except:
    import FireStoreBase

load_dotenv()

class Users(FireStoreBase.Firestore):
    def __init__(self):
        super().__init__()
        self.subcoleccion = 'usuarios'

    def get_users(self):
        try:
            doc_ref = self.db.collection(self.coleccion).document(self.proyecto)
            subcoleccion_ref = doc_ref.collection(self.subcoleccion).stream()

            # Realizar operaciones con los documentos dentro de la subcolección
            salida = {}
            for doc in subcoleccion_ref:
                salida[doc.id] = doc.to_dict()

            return salida

        except Exception as e:
            print(f"Error al acceder a la subcolección: {e}")
            return False

    def create_user(self, datos):
        try:
            doc_ref = self.db.collection(self.coleccion).document(self.proyecto)
            subcoleccion_ref = doc_ref.collection(self.subcoleccion)
            
            # Crear un nuevo documento dentro de la subcolección
            nuevo_doc_ref = subcoleccion_ref.document()
            nuevo_doc_ref.set(datos)
            
            print("Documento creado exitosamente en la subcolección.")
            return nuevo_doc_ref.id
            
        except Exception as e:
            print(f"Error al crear el documento en la subcolección: {e}")
            return None

    def delete_user(self, user:str) -> bool:
        try:
            doc_ref = self.db.collection(self.coleccion).document(self.proyecto)
            subcoleccion_ref = doc_ref.collection(self.subcoleccion)
        
            # Realizar una consulta para obtener los documentos que cumplen con la condición
            query = subcoleccion_ref.where('username', '==', user).get()
        
            # Eliminar los documentos que cumplen con la condición
            for doc in query:
                doc.reference.delete()
                print(f"Usuario '{user}' eliminado de la subcolección.")
        
            return True
        
        except Exception as e:
            print(f"Error al eliminar documentos de la subcolección por campo: {e}")
            return False
    
if __name__ == '__main__':
    firestore_crud = Users()

    salida = firestore_crud.get_users()
    print(salida)

    usuarios = {"username": 'jorge', "password": "Hola"}
    salida = firestore_crud.create_user('contextos', 'Compumax', 'usuarios', usuarios)
    print(salida)