# Flupi

![Flupi icon](home/static/logo.jpeg)

# Bienvenidos

Este es Flupi es un asistente virtual para la Empresa CompuMax, este es el código fuente.

## Requisitos
Instala las dependencias de Python para poder desplegarlo.

``` bash
pip3 install -r requeriments.txt
```

# Uso

Para usar el bot tienes que realizar los siguientes pasos:

- Crear un archivo llamado `.env` con la siguiente información de tu proyecto.
``` bash
GPT=Tu token
API_ROUTE=Api a consultar
FLASK_KEY=@admin
ADMIN_KEY=admin
API_KEY=admin

NOMBRE=Edumax (Nombre con el que se guardara en la base de datos)
DB=contextos (Colección que usaremos)
DEBUG=True

JSON_GCS=tokens/my-token.json

```

> Importante, crear el directorio `tokens/` aquí debe guardar el token para usar los servicios de Firebase.


-----

# Descripción del proyecto 
Dentro de cada modulo de este programa se encuentra una estructura similar a esta: 

``` bash
├── api # Nombre del modulo
│   ├── __init__.py
│   ├── logic.py # Este modulo tiene la lógica separada
│   ├── routes.py # Las rutas con sus respectivos métodos
│   ├── static # Directorio para los archivos estáticos
│   │   ├── info.json
│   │   └── style.css
│   └── templates # Directorio para las plantillas HTML
│       └── api_information.html 
```

Esta estructura es similar para todas las apps del programa, la única excepción es el modulo `databases` en el cual todos son scripts para la conexión con `Firebase`.

## Directorio `configs`
Este es uno de los directorios más complejos, debido a que desde el mismo se realizan las modificaciones de la `API`, teniendo la siguiente estructura:

``` bash
├── configs
│   ├── __init__.py
│   ├── api_compumax.py # Peticiones API de productos 
│   ├── chatbot.py # Aquí dentro se configuran los comandos
│   ├── chatgpt.py # Uso de GPT para las respuestas
│   ├── routes.py # Rutas para acceder a las diferentes configuraciones 
│   ├── voice.py # Crear Audios con el texto generado
│   ├── static
│   │   ├── scripts_context.js
│   │   ├── scripts_images.js
│   │   └── style_images.css
│   ├── templates
│   │   ├── change_images.html
│   │   ├── context.html
│   │   └── home_config.html
``` 