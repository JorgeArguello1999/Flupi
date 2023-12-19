from gtts import gTTS
import os

dir = "./static/audio_chatbot/"
def speaker(texto:str):
    """
    :texto -> Lo que va a decir
    Texto a voz
    """
    # Crear un objeto gTTS
    tts = gTTS(text=texto, lang='es')

    nombre_archivo = "texto_a_voz.mp3"
    tts.save(f"{dir}{nombre_archivo}")

    return nombre_archivo

def clean(nombre_archivo:str):
    # Eliminamos el archivo de audio generado
    try:
        os.remove(nombre_archivo)
        return True
    except FileNotFoundError as error:
        print(f"Error: {error}")
        return False

if __name__ == "__main__":
    salida = speaker("Hola como estas?")
    print(salida)