import sqlite3

def get_context(name:str)-> str:
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

if __name__ == "__main__":
    salida = get_context("no_producto")
    print(salida)