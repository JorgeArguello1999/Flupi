import network, urequests, os, time, uos

def separador(function):
    def beatu():
        print("=======================================")
        function()
        print("=======================================")
    return beatu

@separador
def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(
        "JorgeArguello",
        "pisoarriba"
    )

    while not wlan.isconnected():
        pass

    print("Dirección IP:", wlan.ifconfig()[0])

@separador
def listar_contenido():
    print("Contenido del directorio:")
    for elemento in os.listdir('/'):
        print(elemento)

@separador
def space_free():
    # Obtener estadísticas del sistema de archivos
    estadisticas_fs = uos.statvfs('/')

    # Imprimir la información
    print(f"Espacio total: {estadisticas_fs[0]*estadisticas_fs[2]} bytes")
    print(f"Espacio utilizado: {estadisticas_fs[0]*(estadisticas_fs[2]-estadisticas_fs[3])} bytes")
    print(f"Espacio libre: {estadisticas_fs[0]*estadisticas_fs[3]} bytes")

def _start():
    # Conectar a la red Wi-Fi
    space_free()
    listar_contenido()
    conectar_wifi()

    # URL para la solicitud POST
    url = 'http://192.168.1.12:5000/chatbot/'
    data = {"ask": "Hola Maxi", "device": "computer"}

    try:
        # Realizar la solicitud POST
        response = urequests.post(url, json=data)
        print(f'Código de estado: {response.status_code}')
        # print(f'Contenido de la respuesta: {response.text}')
        response.close()

        # Esperar 10 segundos antes de volver a realizar la solicitud POST y listar el contenido
        time.sleep(10)

    except OSError as e:
        print("Error de conexión:", e)

_start()
