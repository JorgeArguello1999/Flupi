from firebase_admin import credentials, firestore
from dotenv import load_dotenv

import firebase_admin
import os 

load_dotenv()
nombre_proyecto = os.environ.get('NOMBRE') 

# Inicializa la app de Firebase
cred = credentials.Certificate(os.environ.get('JSON_CGS'))
firebase_admin.initialize_app(cred)

# Obtiene una instancia de Firestore
db = firestore.client()

# Lista todas las colecciones en tu base de datos Firestore
collections = db.collections()

# Referencia a la colección
coleccion_ref = db.collection('contextos')

# Obtiene todos los documentos de la colección
documentos = coleccion_ref.stream()

# Itera sobre los documentos e imprime su contenido
for documento in documentos:
    print(f'Documento ID: {documento.id}')
    print(f'Datos: {documento.to_dict()}')


def get_data():
    pass