import pymysql

class connect:
    def __init__(self, host:str, port:int, db:str, user:str, passwd:str):
        """
        :host -> IP de la base de datos
        :port -> Puerto de la base de datos
        :db -> Base de datos a usar
        :user -> Usuario de la base de datos
        :passwd -> Contraseñan para la base de datos
        """
        self.conn = pymysql.connect(
            host = host,
            db = db,
            port = port,
            user = user,
            passwd = passwd 
        )

    def search(self, id_producto:int) -> list:
        """
        :id_producto -> Colocar el id del producto
        """
        try:
            cursor = self.conn.cursor()
            query = f"SELECT * FROM items WHERE id = {id_producto}"
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
    database = connect(
        host="127.0.0.1",
        db="articulos",
        port=3306,
        user="root",
        passwd="root"
    )
    salida = database.search(7092)
    print(salida)