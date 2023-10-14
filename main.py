from modules import voice_text, text_voice, chatgpt
from modules import comandos
import os 

token = os.environ.get("GPT")
nombre = comandos.nombre

while True:
    voz = voice_text.microphone()
    comando = comandos.functions(voz)
    print(voz)

    if nombre in voz:
        if comando != None:
            text_voice.speaker(comando)
        else:
            text_voice.speaker(chatgpt.answer(token=token, context=voz))