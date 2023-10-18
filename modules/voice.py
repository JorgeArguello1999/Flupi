from gtts import gTTS
import speech_recognition as sr
import os

r = sr.Recognizer()

def speaker(texto:str):
    """
    :texto -> Lo que va a decir
    Texto a voz
    """
    # Crear un objeto gTTS
    tts = gTTS(text=texto, lang='es')

    nombre_archivo = "texto_a_voz.mp3"
    tts.save(nombre_archivo)

    try:
        os.system("mpg123 " + nombre_archivo)
    except:
        os.system("start " + nombre_archivo)
    
    return clean(nombre_archivo)

def clean(nombre_archivo:str):
    # Eliminamos el archivo de audio generado
    try:
        os.remove(nombre_archivo)
        return True
    except FileNotFoundError as error:
        print(f"Error: {error}")
        return False

def microphone():
    """
    Obtenemos la entrada del microfono
    """
    with sr.Microphone() as source:
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio, language='es-EC')

        except Exception as e:
            text = ""
            print(f"Error: {e}")

    return text


if __name__ == "__main__":
    microphone()
    salida = speaker("Hola como estas?")
    print(salida)