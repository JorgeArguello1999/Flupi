import firebase_admin
from firebase_admin import credentials, db

# Inicializa la app de Firebase
cred = credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-project-id.firebaseio.com'
})

# Referencia a la base de datos
ref = db.reference('/')

# Ejemplo de escritura de datos
ref.child('users').child('user_id').set({
    'name': 'John Doe',
    'email': 'johndoe@example.com'
})

# Ejemplo de lectura de datos
snapshot = ref.child('users').child('user_id').get()
print(snapshot.val())  # Imprime los datos leídos