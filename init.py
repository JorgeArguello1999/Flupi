from firebase_admin import firestore

# Obtener la instancia del cliente de Firebase Firestore
db = firestore.client()

# Estructura deseada (esto es un ejemplo, debes ajustarlo según tu caso)
estructura_deseada = {
    "Proyecto": {
        "alarm": 0,
        "ips": ["192.168.1.1", "182.12.12.3"],
        "fotos": {
            "chatbot": "foto_base64",
            "usuario": "foto_base64"
        },
        "mensajes": {
            "entender_consulta": "texto",
            "general": "texto",
            "no_producto": "texto"
        },
        "usuarios": {
            "id_automatico_1": {
                "username": "ejemplo",
                "password": "password_encriptada",
                "token": "token"
            },
            "id_automatico_2": {
                "username": "ejemplo",
                "password": "password_encriptada",
                "token": "token"
            }
        }
    }
}

def check_database_structure():
    # Obtener la estructura actual de la base de datos
    estructura_actual = {}  # Aquí obtén la estructura actual de tu base de datos desde Firebase

    # Comparar estructura deseada con la estructura actual
    for coleccion, documentos in estructura_deseada.items():
        if coleccion not in estructura_actual:
            # La colección no existe, crearla
            db.collection(coleccion).document().set({})  # Puedes ajustar los datos que desees inicializar

        for doc, datos in documentos.items():
            if doc not in estructura_actual.get(coleccion, {}):
                # El documento no existe en la colección, crearlo
                db.collection(coleccion).document(doc).set(datos)  # Puedes ajustar los datos que desees inicializar

# Ejecutar la función para verificar y actualizar la estructura al arrancar el proyecto
# check_database_structure()
