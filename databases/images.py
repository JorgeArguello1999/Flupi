import sqlite3
import base64

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
    print(get_image('usuario'))