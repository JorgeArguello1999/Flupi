from modules import camera, voice

# Saluda a personas que conoce
def saludar():
    """
    Devuelve un True cuando reconoce a alguien, y un False cuando no reconoce a nadie
    """
    salida = camera.recognite()
    if salida != "Desconocido":
        voice.speaker(f"¡Hola {salida}! Bienvenido a CompuMax ")
        return True
    else:
        voice.speaker(f"¡Hola!, Bienvenido a Compumax")
        return False

if __name__ == "__main__":
    salida = saludar()
    print(salida)
