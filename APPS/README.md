# Interface Gráfica y parte del ESP32
Al momento de insertar la URL en la ejecución del programa, tener en cuenta que este debe ser la ruta del chatbot

> Ejemplo:
```bash
url = "0.0.0.0:5000/chatbot/"
```
La ruta debe ser colocada de esa manera para que funcione de manera correcta

# ESP32
Para el esp32 existe un `.bin` este es para flashear el ESP32 con MicroPython, no borrarlo, aparte esta el script de 
MicroPython

> Esta es una versión aun en pruebas

# Desktop
Aplicativo de escritorio para el uso del bot

## LINUX
En caso de ejecutar para Linux, tener en cuenta tener instalado lo siguiente:

```bash
sudo apt-get install python3-dbus libnotify-bin
```

# Modificaciones Opcionales
```python
# Función para interactuar con el chatbot a través de API
def api_chatbot(texto: str, url: str) -> None:
    if texto != False and "Maxi" in texto: # -> Aqui modificar el nombre manualmente

# ...

if __name__ == "__main__":
    while True:
        texto = reconocer_voz()
        api_chatbot(texto, "http://127.0.0.1:5000/chatbot/") # -> Modificar la URL
```