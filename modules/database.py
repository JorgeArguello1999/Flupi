import pymysql
import os

def connect_database():
    try:
        conn = pymysql.connect(
            host=os.environ.get("HOST_DB"),
            db=os.environ.get("DATABASE_DB"),
            port=int(os.environ.get("PORT_DB")),
            user=os.environ.get("USER_DB"),
            passwd=os.environ.get("PASSWD_DB")
        )
        return conn
    except Exception as e:
        print("Error al conectar con la base de datos:", e)
        return None


def search_product_by_id(id_producto: int):
    conn = connect_database()
    if conn:
        try:
            cursor = conn.cursor()
            query = f"SELECT * FROM {os.environ.get('TABLE_DB')} WHERE id = {id_producto}"
            cursor.execute(query)
            salida = cursor.fetchall()

            # Recorremos la salida
            respuestas = [data for data in salida]
            return respuestas if respuestas else [[id_producto, "", "No existe"]]
        except Exception as error:
            print("Error al buscar el producto:", error)
            return [[id_producto, "", "Error en la búsqueda"]]
        finally:
            conn.close()
    else:
        return [[id_producto, "", "Error en la conexión"]]


if __name__ == "__main__":
    salida = search_product_by_id(7092)
    print(salida)
