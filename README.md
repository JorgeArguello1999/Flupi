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
