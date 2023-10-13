from modules import voice_text, text_voice

while True:
    if voice_text.microphone():
        respuesta = "Hola como te puedo ayudar?"
        text_voice.speaker(respuesta)