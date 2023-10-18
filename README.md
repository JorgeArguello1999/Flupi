# Flupi

![Flupi icon](Yo/logo.jpeg)

## Holaaaa

Este es Flupi es un asistente virtual para la Empresa CompuMax, este es el código fuente para poder implementarlo

## Requisitos

Debes tener instalado `mpg123` en nuestro sistema (Solo para linux) y tambien instalar las dependencias de Python para el proyecto.

``` bash
sudo apt install mpg123
pip3 install -r requeriments.txt
```

> En caso de usar Windows se usara el programa por defecto que tenga instalado para la reproducción de audio

Aparte tener en cuenta que se debe descargar el fichero [haarcascade_frontalface_default.xml](https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml), este fichero es una configuración para que OpenCV sea capaz de detectar rostros

## Uso

Para usar el bot tienes que realizar los siguientes pasos:

1. Crear una variable de entorno llamada `GPT`

``` bash
export GPT="Tu token de GPT"
echo $GPT
```
