import pymysql

class connect:
    def __init__(self):
        self.conn = pymysql.connect(
            host = "192.168.11.12",
            db = "articulos",
            port = 3306,
            user = "root",
            passwd = "root" 
        )

    def search(self, id_producto:int) -> str:
        """
        :id_producto -> Colocar el id del producto
        """
        cursor = self.conn.cursor()
        query = f"SELECT * FROM items WHERE id = {id_producto}"
        cursor.execute(query)
        return cursor.fetchone()

if __name__ == "__main__":
    database = connect()
    salida = database.search(7092)
    print(salida)
