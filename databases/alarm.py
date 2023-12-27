from firebase_admin import credentials, firestore
from dotenv import load_dotenv

import os
import firebase_admin

# Cargar variables de entorno desde el archivo .env
load_dotenv()

ruta_tokens = os.getenv('JSON_GCS')
cred = credentials.Certificate(ruta_tokens)
firebase_admin.initialize_app(cred)

def obtener_valor_alarm():
    try:
        # Acceder a Firestore
        db = firestore.client()
        subcoleccion_ref = db.collection('contextos').document('Edumax')
        doc = subcoleccion_ref.get()

        if doc.exists:
            data = doc.to_dict()
            valor_alarm = data.get('alarm')
            if valor_alarm is not None:
                return valor_alarm
            else:
                print("El campo 'alarm' no tiene un valor definido.")
                return False
        else:
            print("El documento 'Edumax' no existe.")
            return False
    except Exception as e:
        print(f"Error al obtener el valor de 'alarm': {e}")
        return None
    
def cambiar_estado_alarm(nuevo_estado:bool) -> bool:
    try:
        db = firestore.client()
        subcoleccion_ref = db.collection('contextos').document('Edumax')
        subcoleccion_ref.update({'alarm': nuevo_estado})
        print(f"Estado de 'alarm' actualizado a '{nuevo_estado}'.")
        return True
        
    except Exception as e:
        print(f"Error al cambiar el estado de 'alarm': {e}")
        return False

if __name__ == '__main__':
    valor_alarm = obtener_valor_alarm()
    if valor_alarm is not None:
        print(f"Valor de 'alarm' en la subcolección 'Edumax': {valor_alarm}")
    else:
        print("No se pudo obtener el valor de 'alarm'.")

    nuevo_estado = True  # Reemplaza con el nuevo estado que desees establecer (True o False)
    cambiar_estado_alarm(nuevo_estado)
