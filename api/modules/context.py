import sqlite3

def get_context_all()-> list:
    """
    Obtener lista de todos los contextos
    """
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()
    
    response = cursor.execute(f"SELECT name FROM ContextData")
    response = [row[0] for row in response.fetchall()]
    conn.close()
    return response

def get_context(name:str)-> dict:
    """
    :name -> Contexto a Consultar
    """
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()
    
    response = cursor.execute(f"SELECT content FROM ContextData where name='{name}'")
    response = response.fetchone()
    response = response[0] if response else None
    conn.close()

    return response

def update_context(name:str, text:str)-> bool:
    """
    :name -> Contexto a modificar
    :text -> Texto a Actualizar
    """
    try:
        conn = sqlite3.connect('alarm_status.db')
        cursor = conn.cursor()
        cursor.execute(f'UPDATE ContextData SET content="{text}" WHERE name="{name}"')
        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        print(e)
        return False

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
    print(get_context_all())
    print(get_context("error_mensaje"))

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
