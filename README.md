# Flupi

![Flupi icon](static/logo.jpeg)

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
GPT=tu-token

HOST_DB=127.0.0.1
PORT_DB=3306
USER_DB=root
PASSWD_DB=root
DATABASE_DB=articulos
# Nombre de la tabla donde se encuentran los items a consultar
TABLE_DB=items

```