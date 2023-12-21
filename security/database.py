from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import sqlite3

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

def get_all_users() -> list:
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios')
    users = cursor.fetchall()
    conn.close()
    return users

def search_user(user:str, password:str) -> bool:
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE username = ?', (user,))
    response = cursor.fetchone()
    conn.close()

    if response and check_password_hash(response[2], password):
        return True
    else:
        return False

def get_user_by_username(user:str) -> bool:
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE username = ?', (user,))
    response = cursor.fetchone()
    conn.close()

    if response:
        return response
    else:
        return None

def create_user(username: str, password: str) -> None:
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()
    
    # Cifra la contraseña antes de guardarla en la base de datos
    hashed_password = generate_password_hash(password)
    
    cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

def delete_user_by_id(user_id: int) -> None:
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

create_connection()