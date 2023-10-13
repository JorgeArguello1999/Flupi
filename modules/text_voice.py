from gtts import gTTS
import os

def speaker(texto:str):
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
    try:
        os.remove(nombre_archivo)
        return True
    except FileNotFoundError as error:
        print(f"Error: {error}")
        return False

if __name__ == "__main__":
    salida = speaker("Hola como estas?")
    print(salida)