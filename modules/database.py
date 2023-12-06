import pymysql, os

class connect:
    def __init__(self):
        self.conn = pymysql.connect(
            host=os.environ.get("HOST_DB"), db=os.environ.get("DATABASE_DB"),
            port=int(os.environ.get("PORT_DB")), user=os.environ.get("USER_DB"),
            passwd=os.environ.get("PASSWD_DB")
        )

    def search(self, id_producto:int) -> list:
        """
        :id_producto -> Colocar el id del producto
        """
        try:
            cursor = self.conn.cursor()
            query = f"SELECT * FROM {os.environ.get('TABLE_DB')} WHERE id = {id_producto}"
            cursor.execute(query)
            salida = cursor.fetchall()

            # Recorremos la salida
            respuestas = []
            for data in salida:
                respuestas.append(data)
            return list(data)
        
        except Exception as error:
            print(error)
            return [id_producto, "","No existe"]


if __name__ == "__main__":
    database = connect()
    salida = database.search(7092)
    print(salida)