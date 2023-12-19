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

if __name__ == "__main__":
    salida = get_context("error_mensaje")
    print(salida)

    editar = update_context("error_mensaje", input("Ingresa el contexto: "))
    print(editar)