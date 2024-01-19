# Flupi

![Flupi icon](home/static/logo.jpeg)

## Holaaaa

Este es Flupi es un asistente virtual para la Empresa CompuMax, este es el código fuente para poder implementarlo

## Requisitos
Instala las dependencias de Python para poder desplegarlo.

``` bash
pip3 install -r requeriments.txt
```

## Uso

Para usar el bot tienes que realizar los siguientes pasos:

- Crear un archivo llamado `.env`, o puedes directamente crear las variables en tu entorno

Estas son las variables importantes:
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