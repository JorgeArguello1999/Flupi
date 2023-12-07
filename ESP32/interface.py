import speech_recognition as sr
import requests

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
        return ""

    except sr.RequestError as e:
        print(f"Error en la solicitud: {e}")
        return ""

def api_chatbot(texto:str, url:str) -> str:
    response = requests.post(url, json={
        "ask": texto,
        "device": "bot"
    })

    if response.status_code == 200:
        # Obtener el contenido del archivo de audio
        audio_content = response.content

        # Guardar el archivo de audio
        nombre_archivo = 'audio_recibido.mp3'
        with open(nombre_archivo, 'wb') as archivo_audio:
            archivo_audio.write(audio_content)
            print(f"Archivo de audio guardado como {nombre_archivo}")
    else:
        print("Error al obtener el archivo de audio")


if __name__ == "__main__":
    api_chatbot(
        texto=reconocer_voz(),
        url="http://127.0.0.1:5000/chatbot/"
    )