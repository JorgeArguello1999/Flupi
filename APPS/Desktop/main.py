import speech_recognition as sr
import requests
import pygame

# Crear un objeto Recognizer
recognizer = sr.Recognizer()

# Función para grabar audio desde el micrófono y realizar reconocimiento de voz
def reconocer_voz():
    with sr.Microphone() as source:
        print("Di algo...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Reconociendo...")

        # Usar reconocimiento de voz de Google
        texto = recognizer.recognize_google(audio, language='es-ES')
        print(f"{texto}")

        return texto

    except sr.UnknownValueError:
        print("No se pudo entender lo que dijiste")
        return "Dime que repita lo que dije porque no te escuche"

    except sr.RequestError as e:
        print(f"Error en la solicitud: {e}")
        return "Hubo un Error"

def reproducir_audio(ruta_archivo):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(ruta_archivo)
    pygame.mixer.music.play()

    # Mantener el programa en ejecución hasta que termine la reproducción
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Ajusta la frecuencia de actualización

def api_chatbot(texto:str, url:str) -> str:
    response = requests.post(url, json={
        "ask": texto,
        "device": "bot"
    })

    if response.status_code != 200:
        print("Error al obtener el archivo de audio")

    else:
        # Obtener el contenido del archivo de audio
        audio_content = response.content

        # Guardar el archivo de audio
        nombre_archivo = '_temp_audio.mp3'
        with open(nombre_archivo, 'wb') as archivo_audio:
            archivo_audio.write(audio_content)
            print(f"Archivo de audio guardado como {nombre_archivo}")
    
    reproducir_audio(nombre_archivo)

if __name__ == "__main__":
    while True:
        api_chatbot(
            texto=reconocer_voz(),
            url="http://127.0.0.1:5000/chatbot/"
        )