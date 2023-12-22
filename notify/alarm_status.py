import sqlite3

# Función para inicializar la base de datos
def initialize_db():
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS alarm_status (
        id INTEGER PRIMARY KEY,
        status INTEGER
    )''')
    conn.commit()
    conn.close()

# Función para obtener el estado actual de la alarma desde la base de datos
def get_alarm_status():
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()
    cursor.execute('SELECT status FROM alarm_status WHERE id = 1')
    status = cursor.fetchone()
    conn.close()
    if status:
        return bool(status[0])
    return False

# Función para actualizar el estado de la alarma en la base de datos
def update_alarm_status(status):
    conn = sqlite3.connect('alarm_status.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO alarm_status (id, status) VALUES (?, ?)', (1, int(status)))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
    print(get_alarm_status())