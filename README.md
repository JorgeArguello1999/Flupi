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
GPT=Tu token para GPT
API_ROUTE=ruta_api_para_consultar_precios
DEBUG=false
FLASK_KEY=clave para flask

ADMIN_KEY=esta frase es la que se necesita para eliminar usuarios
NOMBRE= Con esto busca dentro de la base de datos
JSON_CGS= Ruta donde esta el json para firebase

```