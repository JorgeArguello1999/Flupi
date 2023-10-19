# Flupi

![Flupi icon](me/logo.jpeg)

## Holaaaa

Este es Flupi es un asistente virtual para la Empresa CompuMax, este es el código fuente para poder implementarlo

## Requisitos

Debes tener instalado `mpg123` en nuestro sistema (Solo para linux) y tambien instalar las dependencias de Python para el proyecto.

``` bash
sudo apt install mpg123
pip3 install -r requeriments.txt
```

> En caso de usar Windows se usara el programa por defecto que tenga instalado para la reproducción de audio

## Uso

Para usar el bot tienes que realizar los siguientes pasos:

- Crear una variable de entorno llamada `GPT`

``` bash
export GPT="Tu token de GPT"
echo $GPT
```

- En caso de querer usar el reconocimiento facial debes entrenar al modelo, usando las funciones existentes en el módulo `camera.py`, este posee funciones para capturar los rostros, entrenar el modelo y detectar rostros, y aparte una función encargada de detectar cualquier tipo de rostro humano.

### Tener en cuenta de cambiar las IP

Estas IP's se encuentran para la base de datos y para crear el servidor de escucha

En este código esta la conexión a la base de datos `./modules/database.py`

``` python
class connect:
    def __init__(self):
        self.conn = pymysql.connect(
            host = "127.0.0.1", # IP de la base de datos
            db = "articulos", # Nombre de la base de datos
            port = 3306, 
            user = "root", # Usuario
            passwd = "root" # Contraseña
        )
```

Este código muestra el servidor para la llamada al técnico `./modules/server.py`

``` python
# Configuración de dirección del servidor
host = "192.168.11.12"
port = 8080
```
