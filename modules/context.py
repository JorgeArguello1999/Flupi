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

if __name__ == "__main__":
    print(get_context_all())
    print(get_context("error_mensaje"))

    # editar = update_context("error_mensaje", input("Ingresa el contexto: "))
    # print(editar)