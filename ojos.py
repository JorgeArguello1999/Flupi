from modules import camera, voice
import time

count = 0
while True:
    salida = camera.recognite()
    if salida != "Desconocido":
        if count != 0: 
            time.sleep(5)
            voice.speaker(f"Hola {salida}")
        else: 
            voice.speaker(f"Hola {salida}")

        count = count + 1

