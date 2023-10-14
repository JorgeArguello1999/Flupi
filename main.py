import datetime, os
from modules import voice_text, text_voice, chatgpt

# Estos son los comandos, si vas a añadir más comandos 
# ver como entiende las ordenes el voice_text.py
token = os.environ.get("GPT")
nombre = "Maxi"
hora = datetime.datetime.now().strftime("%H:%M")
fecha_actual = datetime.datetime.now()

nombres_meses = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio", 
    8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}
fecha = f"{fecha_actual.day} de {nombres_meses[fecha_actual.month]} de {fecha_actual.year}"


comandos = {
    f"Hola {nombre}": "Hola, en que te puedo ayudar?",
    f"{nombre} qué hora es": f"Hola, la hora es: {hora}",
    f"{nombre} qué fecha es": f"La fecha es: {fecha}"
}

def functions(text:str):
    for com in comandos:
        if text in com:
            return comandos[com]

while True:
    voz = voice_text.microphone()
    comando = functions(voz)
    print(voz)

    if nombre in voz:
        if comando != None:
            text_voice.speaker(comando)
        else:
            text_voice.speaker(chatgpt.answer(token=token, context=voz))