from modules import camera, voice

# Saluda a personas que conoce
def saludar():
    salida = camera.recognite()
    while True:
        if salida != "Desconocido":
            voice.speaker(f"¡Hola {salida}! Bienvenido a CompuMax ")
            break
        else:
            voice.speaker(f"¡Hola!, Bienvenido a Compumax")
            continue

if __name__ == "__main__":
    saludar()
