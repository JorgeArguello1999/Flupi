import sqlite3

# Configuración de la base de datos
def create_connection():
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def search_user(user:str, password:str) -> dict:
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM usuarios WHERE username = "{user}" AND password = "{password}"')
    response = cursor.fetchone()
    conn.close()

    if response:
        return True
    else:
        return False

create_connection()