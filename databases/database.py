from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import sqlite3
import uuid
# Usuarios
def get_all_users() -> list:
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios')
    users = cursor.fetchall()
    conn.close()
    return users

def search_user(user:str, password:str) -> bool:
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE username = ?', (user,))
    response = cursor.fetchone()
    conn.close()

    if response and check_password_hash(response[2], password):
        return True
    else:
        return False

def search_token(token:str) -> bool:
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()
    cursor.execute('SELECT token FROM usuarios WHERE token = ?', (token,))
    response = cursor.fetchone()
    conn.close()

    if response:
        return True
    else:
        return False

def get_user_by_username(user:str) -> bool:
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE username = ?', (user,))
    response = cursor.fetchone()
    conn.close()

    if response:
        return response
    else:
        return None

def create_user(username: str, password: str) -> None:
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()
    
    # Cifra la contraseña antes de guardarla en la base de datos
    hashed_password = generate_password_hash(password)

    # Generamos un token aleatorio para el usuario
    token = str(uuid.uuid4())
    
    cursor.execute("INSERT INTO usuarios (username, password, token) VALUES (?, ?, ?)", (username, hashed_password, token))
    conn.commit()
    conn.close()

def delete_user_by_id(user_id: int) -> None:
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()


# Imagenes
def get_image_all()-> list:
    """
    Obtener lista de todos los contextos
    """
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()
    
    response = cursor.execute(f"SELECT name FROM Fotos")
    response = [row[0] for row in response.fetchall()]
    conn.close()
    return response

def get_image(filename:str):
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT image FROM Fotos WHERE name='{filename}'")
    image_data = cursor.fetchone()

    conn.close()

    if image_data:
        return image_data[0]
    else:
        return 'Image not found'

def update_image(filename:str, image) -> bool:
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE Fotos SET image=? WHERE name=?", (image, filename))
        conn.commit()
        salida = "Imagen actualizada correctamente en la base de datos."
    except sqlite3.Error as e:
        salida = "Error al actualizar la imagen en la base de datos: {e}"
    finally:
        conn.close()
    
    return salida

if __name__ == "__main__":
    # editar = update_context("error_mensaje", input("Ingresa el contexto: "))
    # print(editar)

    import sqlite3

    def read_image(filename):
        # Abre la imagen en modo binario para leer su contenido
        with open(filename, 'rb') as file:
            img_data = file.read()
        return img_data

    def insert_image_into_db(db_file, image_name, image_data):
        # Conecta con la base de datos
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        try:
            # Inserta la imagen en la tabla Fotos
            cursor.execute("INSERT INTO Fotos (name, image) VALUES (?, ?)", (image_name, image_data))
            conn.commit()
            print("Imagen insertada correctamente en la base de datos.")
        except sqlite3.Error as e:
            print(f"Error al insertar la imagen en la base de datos: {e}")
        finally:
            conn.close()

    # Nombre de la base de datos SQLite
    database_file = 'alarm_status.db'

    # Nombre y ruta de la imagen que quieres insertar en la base de datos
    image_path = './uploads/user.jpeg'
    image_name = 'usuario'

    # Lee el contenido binario de la imagen
    image_data = read_image(image_path)

    # Inserta la imagen en la base de datos
    insert_image_into_db(database_file, image_name, image_data)



# Función para inicializar la base de datos
def initialize_db():
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS alarm_status (
        id INTEGER PRIMARY KEY,
        status INTEGER
    )''')
    conn.commit()
    conn.close()

# Notify
# Función para obtener el estado actual de la alarma desde la base de datos
def get_alarm_status():
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()
    cursor.execute('SELECT status FROM alarm_status WHERE id = 1')
    status = cursor.fetchone()
    conn.close()
    if status:
        return bool(status[0])
    return False

# Función para actualizar el estado de la alarma en la base de datos
def update_alarm_status(status):
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO alarm_status (id, status) VALUES (?, ?)', (1, int(status)))
    conn.commit()
    conn.close()

import base64

# Images
def get_image_all()-> list:
    """
    Obtener lista de todos los contextos
    """
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()
    
    response = cursor.execute(f"SELECT name FROM Fotos")
    response = [row[0] for row in response.fetchall()]
    conn.close()
    return response

def get_image(filename:str):
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT image FROM Fotos WHERE name='{filename}'")
    image_data = cursor.fetchone()

    conn.close()

    if image_data:
        # Codificar la imagen en base64
        return base64.b64encode(image_data[0]).decode('utf-8')
    else:
        return 'Image not found'

def update_image(filename:str, image) -> bool:
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE Fotos SET image=? WHERE name=?", (image, filename))
        conn.commit()
        salida = "Imagen actualizada correctamente en la base de datos."
    except sqlite3.Error as e:
        salida = "Error al actualizar la imagen en la base de datos: {e}"
    finally:
        conn.close()
    
    return salida

if __name__ == "__main__":
    salida = search_token('dcfbaac-e8e8-47b4-8493-75232f17a7bd')
    print(salida)