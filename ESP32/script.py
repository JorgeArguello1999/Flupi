import network
import urequests
import os
import time

def conectar_wifi():
    SSID = 'JorgeArguello'
    PASSWORD = 'pisoarriba'

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    while not wlan.isconnected():
        pass

    print("Conexión Wi-Fi establecida. Dirección IP:", wlan.ifconfig()[0])

def listar_contenido_directorio(directorio):
    contenido = os.listdir(directorio)

    print("Contenido del directorio:")
    for elemento in contenido:
        print(elemento)

# Conectar a la red Wi-Fi
conectar_wifi()

# URL para la solicitud POST
url = 'http://192.168.1.12:5000/chatbot/'
data = {"ask": "hola", "device": "computer"}

while True:
    try:
        # Realizar la solicitud POST
        response = urequests.post(url, json=data)
        print('Código de estado:', response.status_code)
        print('Contenido de la respuesta:')
        print(response.text)
        response.close()

        # Listar el contenido del directorio raíz
        directorio = '/'
        listar_contenido_directorio(directorio)

        # Esperar 10 segundos antes de volver a realizar la solicitud POST y listar el contenido
        time.sleep(10)
    except OSError as e:
        print("Error de conexión:", e)

