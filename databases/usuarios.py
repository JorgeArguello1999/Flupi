from firebase_admin import credentials, firestore
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from dotenv import load_dotenv

import os 
import uuid
import firebase_admin

load_dotenv()

# Configuración inicial
ruta = os.environ.get('JSON_GCS')
nombre = os.environ.get('NOMBRE')
coleccion = 'contextos'

# Inicializa la app de Firebase
cred = credentials.Certificate(ruta)
firebase_admin.initialize_app(cred) 

def create_user(username: str, password: str) -> bool:
    # Cifra la contraseña antes de guardarla en la base de datos
    hashed_password = generate_password_hash(password)
    # Generamos un token aleatorio para el usuario
    token = str(uuid.uuid4())

    db = firestore.client()
    try:
        ref = db.collection(coleccion).document(nombre)
        usuario = ref.collection('usuarios')

        usuario.add({
            'username': username,
            'password': hashed_password,
            'token': token
        })

        return True
    except Exception as e:
        return False

def get_user_by_name(usuario):
    db = firestore.client()
    try:
        compumax_ref = db.collection(coleccion).document(nombre)
        usuarios_ref = compumax_ref.collection('usuarios')
        
        # Realiza la consulta usando el método 'where' para filtrar por el nombre de usuario
        query = usuarios_ref.where('username', '==', usuario).limit(1)
        results = query.stream()

        user_info = None
        for doc in results:
            user_info = doc.to_dict()
            break  # Obtiene solo el primer usuario encontrado
        return user_info

    except Exception as e:
        print(f"Error al obtener el usuario: {e}")
        return None


def get_all_users() -> list:
    try:
        # Referencia a la colección 'usuarios' en Firestore
        db = firestore.client()
        usuarios_ref = db.collection('usuarios')
        users = usuarios_ref.get()
        user_list = []

        for user in users:
            user_list.append(user.to_dict())

        return user_list

    except Exception as e:
        print(f"Error al obtener usuarios de Firestore: {e}")
        return []

def search_user(user: str, password: str) -> bool:
    try:
        # Obtener usuario de Firestore por nombre de usuario
        user_info = get_user_by_name(user)

        if user_info and check_password_hash(user_info.get('password', ''), password):
            return True
        else:
            return False
    except Exception as e:
        print(f"Error en la búsqueda de usuario: {e}")
        return False

if __name__ == "__main__":
    users = get_all_users()
    print(f'Usuarios: {users}')

    # salida = create_user(username="jorge", password="jorge")

    salida = get_user_by_name("jorge")
    print(salida)

    salida = search_user(user='jorge', password='32768:8:1$zRQCfeXlZ1ZJdlsy$740c92b01d45e1c707b1ec0a31593553fb4ec14791b98ceb1fbd8a9eeab3bd20ea366c78e616f43c5e18c6f7fd2e2a94861e3c2722ac3d2c1b284f3ca87521ca')
    print(salida)