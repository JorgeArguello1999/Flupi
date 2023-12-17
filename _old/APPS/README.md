# Datos importantes
Al momento de usar el Bot, tener en cuenta que este tiene un archivo de configuración llamado `config.txt` que tiene la siguiente estructura:
> Ejemplo:
```json
{
    "name": "Maxi",
    "url": "http://127.0.0.1:5000/chatbot/"
}
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
# Esto es para las notificaciones en linux
```