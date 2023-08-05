import pymysql
import os

class connect:
    def __init__(self):
        db_passwd = os.getenv("PASSWD_DB")
        self.conn = pymysql.connect(
            host = "192.168.1.11",
            db = "flupi_db",
            port = 3306,
            user = "root",
            passwd = db_passwd
        )

    def list(self):
        cursor = self.conn.cursor()
        query = "select sum(avengers) as Avengers, sum(quimbolitos) as Quimbolitos from points;"
        cursor.execute(query)
        return cursor.fetchone()

    def list_all(self):
        cursor = self.conn.cursor()
        query = "select * from points"
        cursor.execute(query)
        return cursor.fetchall()

    def insert(self, datos):
        """
        Insertar datos por medio de array
        donde se especifique la siguiente estructura

        datos = [1, 1]

        Primer = Avengers
        Segundo = Quimbolitos

        | Categoría     | Avengers | Quimbolitos | Fecha |
        |-------------- | -------- | ----------- | ----- |
        | Puntos Semana 1 | 150      | 120         | 2023-07-01 |
        | Puntos Semana 2 | 200      | 180         | 2023-07-01 |
        """
        cursor = self.conn.cursor()
        query = f"""
        insert into points (avengers, quimbolitos, usuario) values(
            {datos[0]}, {datos[1]}, '{datos[2]}'
        );
        """
        try:
            cursor.execute(query)
            self.conn.commit()
            return True
        except pymysql.DatabaseError as e:
            print(e)
            return False 

    def remove(self, id):
        cursor = self.conn.cursor()
        query = f'delete from points where id={id}'
        print(query)
        try:
            cursor.execute(query)
            self.conn.commit()
            return True
        except pymysql.DatabaseError as e:
            print(e)
            return False 
        

if __name__ == "__main__":
    con = connect()
    print(con.list())

