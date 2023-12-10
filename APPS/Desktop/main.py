import speech_recognition as sr
import requests
import pygame
import os
from plyer import notification

# Notificar lo que detecto
def notificacion(titulo:str, mensaje:str):
    notification.notify(
        title=titulo,
        message=mensaje,
        app_name='Bot',  
        timeout=10  
    )

# Leemos el Archivo config.txt
def obtener_url_desde_config():
    try:
        with open("config.txt", "r") as archivo_config:
            url = archivo_config.read().strip()
            return url

    except FileNotFoundError:
        print("El archivo de configuración no existe")
        return None

# Función para grabar audio desde el micrófono y realizar reconocimiento de voz
def reconocer_voz():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Di algo...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Reconociendo...")

        # Usar reconocimiento de voz de Google
        texto = recognizer.recognize_google(audio, language='es-ES')
        notificacion(titulo="Bot", mensaje=f"{texto}")

        return texto

    except sr.UnknownValueError:
        print("No se pudo entender lo que dijiste")
        return False

    except sr.RequestError as e:
        print(f"Error en la solicitud: {e}")
        return False

# Función para reproducir archivo de audio
def reproducir_audio(ruta_archivo):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(ruta_archivo)
    pygame.mixer.music.play()

    # Mantener el programa en ejecución hasta que termine la reproducción
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10) 

    pygame.mixer.music.stop()
    pygame.quit()

# Función para interactuar con el chatbot a través de API
def api_chatbot(texto: str, url: str) -> None:
    if texto != False and "Maxi" in texto:
        try:
            response = requests.post(url, json={"ask": texto, "device": "bot"})

            if response.status_code != 200:
                print("Error al obtener el archivo de audio")
                return

            # Obtener el contenido del archivo de audio
            audio_content = response.content

            # Guardar el archivo de audio temporalmente
            nombre_archivo = '_temp_audio.mp3'
            with open(nombre_archivo, 'wb') as archivo_audio:
                archivo_audio.write(audio_content)
                print(f"Archivo de audio guardado como {nombre_archivo}")

            reproducir_audio(nombre_archivo)

        except requests.RequestException as e:
            print(f"Error en la solicitud al chatbot: {e}")

        finally:
            if os.path.exists(nombre_archivo):
                # Eliminar archivo de audio temporal si existe
                os.remove(nombre_archivo)  

if __name__ == "__main__":
    while True:
        texto = reconocer_voz()
        # Obtener la URL desde el archivo de configuración
        url = obtener_url_desde_config()
        
        if url:
            api_chatbot(texto, url)
        else:
            print("No se pudo obtener la URL de la API desde el archivo de configuración.")